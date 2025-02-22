from random import randint

from task_two.cell import Cell

class GamePole:
    def __init__(self, N, M):
        self.N = N
        self.M = M
        self.pole = [[Cell() for _ in range(N)] for _ in range(N)]
        self.init()


    def init(self):
        for row in self.pole:
            for cell in row:
                cell.mine = False
                cell.around_mines = 0
                cell.fl_open = False

        mines_set = 0
        while mines_set < self.M:
            x, y = randint(0, self.N - 1), randint(0, self.N - 1)
            if not self.pole[x][y].mine:
                self.pole[x][y].mine = True
                mines_set += 1

        for x in range(self.N):
            for y in range(self.N):
                if not self.pole[x][y].mine:
                    self.pole[x][y].around_mines = self.count_mines_around(x, y)


    def count_mines_around(self, x, y):
        """Возвращает количество мин вокруг клетки"""
        mines = 0
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.N and 0 <= ny < self.N and self.pole[nx][ny].mine:
                    mines += 1
        return mines


    def show(self):
        """Отображает поле в консоли"""
        print("  " + " ".join(str(i) for i in range(self.N)))
        for i, row in enumerate(self.pole):
            line = []
            for cell in row:
                if cell.fl_open:
                    if cell.mine:
                        line.append("*")
                    else:
                        line.append(str(cell.around_mines) if cell.around_mines > 0 else " ")
                else:
                    line.append("#")
            print(f"{i} {' '.join(line)}")


    def open_cell(self, x, y):
        """Открывает клетку на поле."""
        if 0 <= x < self.N and 0 <= y < self.N and not self.pole[x][y].fl_open:
            self.pole[x][y].fl_open = True
            if self.pole[x][y].mine:
                print("БУМ! Игра окончена.")
                self.show()
                exit()
            elif self.pole[x][y].around_mines == 0:
                for dx in (-1, 0, 1):
                    for dy in (-1, 0, 1):
                        if dx != 0 or dy != 0:
                            self.open_cell(x + dx, y + dy)


    def check_win(self):
        """Проверяет, победил ли игрок."""
        for row in self.pole:
            for cell in row:
                if not cell.fl_open and not cell.mine:
                    return False  # Есть ещё закрытые безопасные клетки
        return True
