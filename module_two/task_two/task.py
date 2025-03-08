import requests
import pandas as pd
import re
from bs4 import BeautifulSoup
from datetime import datetime, timezone
from sqlalchemy.exc import IntegrityError
from table import SpimexTradingResult, engine, session

BASE_URL = "https://spimex.com"
RESULTS_URL = "https://spimex.com/markets/oil_products/trades/results/"
START_YEAR = 2023


def get_all_bulletin_page_urls():
    """ Получает ссылки на все бюллетени """
    page_data = []
    page_number = 1

    while True:
        page_url = f"{RESULTS_URL}?page=page-{page_number}" if page_number > 1 else RESULTS_URL
        response = requests.get(page_url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        new_data_found = False

        for link in soup.find_all("a", href=True):
            if "Бюллетень по итогам торгов в Секции «Нефтепродукты»" in link.text:
                date_span = link.find_next("span")
                if date_span and date_span.text.strip():
                    match = re.search(r"(\d{2})\.(\d{2})\.(\d{4})", date_span.text.strip())
                    if match:
                        day, month, year = match.groups()
                        trade_date = datetime(int(year), int(month), int(day))
                        if trade_date.year < START_YEAR:
                            return page_data
                        page_url = BASE_URL + link['href']
                        page_data.append((page_url, trade_date))
                        new_data_found = True

        if not new_data_found:
            break

        page_number += 1

    return page_data


def download_and_parse_bulletin(url):
    """ Скачивает и парсит бюллетень """
    response = requests.get(url)
    response.raise_for_status()

    file_path = "bulletin.xls"
    with open(file_path, "wb") as f:
        f.write(response.content)

    try:
        df_dict = pd.read_excel(file_path, sheet_name=None, engine="xlrd", header=None)
    except Exception as e:
        return None

    for sheet_name, data in df_dict.items():
        for i, row in data.iterrows():
            for cell in row:
                if isinstance(cell, str) and "Единица измерения: Метрическая тонна" in cell:
                    df_clean = data.iloc[i + 1:].reset_index(drop=True)
                    df_clean.columns = df_clean.iloc[0]
                    df_clean = df_clean[1:].reset_index(drop=True)
                    df_clean.columns = df_clean.columns.astype(str).str.replace('\n', ' ').str.strip()
                    return df_clean

    return None


def process_data(df, trade_date):
    """ Обрабатывает и нормализует данные """
    expected_columns = ['Код Инструмента', 'Наименование Инструмента', 'Базис поставки',
                        'Объем Договоров в единицах измерения', 'Обьем Договоров, руб.', 'Количество Договоров, шт.']

    missing_columns = [col for col in expected_columns if col not in df.columns]
    if missing_columns:
        return None

    df['Количество Договоров, шт.'] = df['Количество Договоров, шт.'].astype(str).str.replace(',', '').str.strip()
    df['Количество Договоров, шт.'] = pd.to_numeric(df['Количество Договоров, шт.'], errors='coerce').fillna(0).astype(
        int)
    df = df[df['Количество Договоров, шт.'] > 0]

    df = df.rename(columns={
        'Код Инструмента': 'exchange_product_id',
        'Наименование Инструмента': 'exchange_product_name',
        'Базис поставки': 'delivery_basis_name',
        'Объем Договоров в единицах измерения': 'volume',
        'Обьем Договоров, руб.': 'total',
        'Количество Договоров, шт.': 'count'
    })

    df['oil_id'] = df['exchange_product_id'].astype(str).str[:4]
    df['delivery_basis_id'] = df['exchange_product_id'].astype(str).str[4:7]
    df['delivery_type_id'] = df['exchange_product_id'].astype(str).str[-1]
    df['date'] = trade_date
    df['created_on'] = datetime.now(timezone.utc)
    df['updated_on'] = datetime.now(timezone.utc)

    return df[['exchange_product_id', 'exchange_product_name', 'oil_id', 'delivery_basis_id', 'delivery_basis_name',
               'delivery_type_id', 'volume', 'total', 'count', 'date', 'created_on', 'updated_on']]


def save_to_db(df):
    """ Сохраняет данные в БД """

    for _, row in df.iterrows():
        record = SpimexTradingResult(**row.to_dict())
        try:
            session.add(record)
            session.commit()
        except IntegrityError:
            session.rollback()
    session.close()


if __name__ == "__main__":
    bulletin_data = get_all_bulletin_page_urls()
    if bulletin_data:
        for url, trade_date in bulletin_data:
            raw_data = download_and_parse_bulletin(url)
            if raw_data is not None:
                processed_data = process_data(raw_data, trade_date)
                if processed_data is not None:
                    save_to_db(processed_data)
    else:
        print("Нет новых бюллетеней для обработки")
