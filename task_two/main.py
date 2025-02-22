from task_two.game_pole import GamePole

if __name__ == "__main__":
    N = 10  # Размер поля
    M = 12  # Количество мин
    game = GamePole(N, M)

    print("Введите координаты клетки (через пробел), чтобы открыть её.")

    while True:
        game.show()
        try:
            x, y = map(int, input("Введите координаты (x y): ").split())
            game.open_cell(x, y)

            if game.check_win():
                print("Победа")
                game.show()
                break
        except (ValueError, IndexError):
            print("Ошибка! Введите два целых числа в пределах игрового поля.")