import curses

from life import GameOfLife
from ui import UI


class Console(UI):
    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)

    def draw_borders(self, screen) -> None:
        """ Отобразить рамку. """
        screen.border()

    def draw_grid(self, screen) -> None:
        """ Отобразить состояние клеток. """
        for row_num in range(len(self.life.curr_generation)):
            for column_num in range(len(self.life.curr_generation[row_num])):
                cell_status = self.life.curr_generation[row_num][column_num]
                if cell_status == 1:
                    screen.addch(row_num + 1, column_num + 1, "*")
                elif cell_status == 0:
                    screen.addch(row_num + 1, column_num + 1, " ")

    def run(self) -> None:
        screen = curses.initscr()
        while True:
            self.draw_borders(screen)
            self.draw_grid(screen)
            screen.refresh()
            import time

            time.sleep(1)
            self.life.step()
