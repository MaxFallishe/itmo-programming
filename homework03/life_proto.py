import pygame  # type: ignore
import random

from pygame.locals import *  # type: ignore
from typing import List, Tuple

Cell = Tuple[int, int]
Cells = List[int]
Grid = List[Cells]


class GameOfLife:
    def __init__(
        self, width: int = 640, height: int = 480, cell_size: int = 10, speed: int = 10
    ) -> None:
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        # self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Скорость протекания игры
        self.speed = speed

        # Создание двумерного списка сетки игрового поля
        self.grid = self.create_grid()

    def draw_lines(self) -> None:
        """ Отрисовать сетку """
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(
                self.screen, pygame.Color("black"), (x, 0), (x, self.height)
            )
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(
                self.screen, pygame.Color("black"), (0, y), (self.width, y)
            )

    def run(self) -> None:
        """ Запустить игру """
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))

        # Создание списка клеток
        # PUT YOUR CODE HERE

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:  # type: ignore
                    running = False
            self.draw_grid()
            self.draw_lines()

            # Отрисовка списка клеток
            # Выполнение одного шага игры (обновление состояния ячеек)
            # PUT YOUR CODE HERE
            self.grid = self.get_next_generation()
            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def create_grid(self, randomize: bool = False) -> Grid:
        """
        Создание списка клеток.

        Клетка считается живой, если ее значение равно 1, в противном случае клетка
        считается мертвой, то есть, ее значение равно 0.

        Parameters
        ----------
        randomize : bool
            Если значение истина, то создается матрица, где каждая клетка может
            быть равновероятно живой или мертвой, иначе все клетки создаются мертвыми.

        Returns
        ----------
        out : Grid
            Матрица клеток размером `cell_height` х `cell_width`.
        """
        if randomize:
            grid = [
                [random.randint(0, 1) for i in range(self.cell_width)]
                for i in range(self.cell_height)
            ]
        else:
            grid = [
                [0 for i in range(self.cell_width)] for i in range(self.cell_height)
            ]
        return grid

    def draw_grid(self) -> None:
        """1
        Отрисовка списка клеток с закрашиванием их в соответствующе цвета.
        """
        for cube_y_coordinate in range(len(self.grid[0])):
            for cube_x_coordinate in range(len(self.grid)):
                if self.grid[cube_x_coordinate][cube_y_coordinate] == 1:
                    cell_color = "green"
                else:
                    cell_color = "white"
                pygame.draw.rect(
                    self.screen,
                    pygame.Color(cell_color),
                    (
                        cube_y_coordinate * self.cell_size,
                        cube_x_coordinate * self.cell_size,
                        self.cell_size,
                        self.cell_size,
                    ),
                )

    def get_neighbours(self, cell: Cell) -> Cells:
        """
        Вернуть список соседних клеток для клетки `cell`.

        Соседними считаются клетки по горизонтали, вертикали и диагоналям,
        то есть, во всех направлениях.

        Parameters
        ----------
        cell : Cell
            Клетка, для которой необходимо получить список соседей. Клетка
            представлена кортежем, содержащим ее координаты на игровом поле.

        Returns
        ----------
        out : Cells
            Список соседних клеток.
        """
        neighbours_cells_values = []
        for i in range(cell[0] - 1, cell[0] + 1 + 1):
            for j in range(cell[1] - 1, cell[1] + 1 + 1):
                if i == cell[0] and j == cell[1]:
                    pass
                else:
                    if 0 <= i < len(self.grid):
                        if 0 <= j < len(self.grid[0]):
                            neighbours_cells_values.append(self.grid[i][j])

        return neighbours_cells_values

    def get_next_generation(self) -> Grid:
        """
        Получить следующее поколение клеток.

        Returns
        ----------
        out : Grid
            Новое поколение клеток.
        """
        updated_grid = [i[:] for i in self.grid]
        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                cell = (i, j)
                cell_status = self.grid[i][j]
                count_of_alive_neighbours = sum(self.get_neighbours(cell))
                if cell_status == 1:
                    if count_of_alive_neighbours == 2 or count_of_alive_neighbours == 3:
                        pass
                    else:
                        updated_grid[i][j] = 0

                elif cell_status == 0:
                    if count_of_alive_neighbours == 3:
                        updated_grid[i][j] = 1
                    else:
                        pass

        return updated_grid
