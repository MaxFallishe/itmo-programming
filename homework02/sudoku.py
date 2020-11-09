from typing import Tuple, List, Set, Optional


def read_sudoku(filename: str) -> List[List[str]]:
    """ Прочитать Судоку из указанного файла """
    digits = [c for c in open(filename).read() if c in "123456789."]
    grid = group(digits, 9)
    return grid


def display(grid: List[List[str]]) -> None:
    """Вывод Судоку """
    width = 2
    line = "+".join(["-" * (width * 3)] * 3)
    for row in range(9):
        print(
            "".join(
                grid[row][col].center(width) + ("|" if str(col) in "25" else "")
                for col in range(9)
            )
        )
        if str(row) in "25":
            print(line)
    print()


def group(values: List[str], n: int) -> List[List[str]]:
    """
    Сгруппировать значения values в список, состоящий из списков по n элементов

    >>> group([1,2,3,4], 2)
    [[1, 2], [3, 4]]
    >>> group([1,2,3,4,5,6,7,8,9], 3)
    [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    """
    split_list = [values[i : i + n] for i in range(0, len(values), n)]
    return split_list


def get_row(grid: List[List[str]], pos: Tuple[int, int]) -> List[str]:
    """Возвращает все значения для номера строки, указанной в pos

    >>> get_row([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '2', '.']
    >>> get_row([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (1, 0))
    ['4', '.', '6']
    >>> get_row([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (2, 0))
    ['.', '8', '9']
    """
    row_content = grid[pos[0]]
    return row_content


def get_col(grid: List[List[str]], pos: Tuple[int, int]) -> List[str]:
    """Возвращает все значения для номера столбца, указанного в pos

    >>> get_col([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '4', '7']
    >>> get_col([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (0, 1))
    ['2', '.', '8']
    >>> get_col([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (0, 2))
    ['3', '6', '9']
    """
    column_content = [i[pos[1]] for i in grid]
    return column_content


def get_block(grid: List[List[str]], pos: Tuple[int, int]) -> List[str]:
    """Возвращает все значения из квадрата, в который попадает позиция pos

    >>> grid = read_sudoku('puzzle1.txt')
    >>> get_block(grid, (0, 1))
    ['5', '3', '.', '6', '.', '.', '.', '9', '8']
    >>> get_block(grid, (4, 7))
    ['.', '.', '3', '.', '.', '1', '.', '.', '6']
    >>> get_block(grid, (8, 8))
    ['2', '8', '.', '.', '.', '5', '.', '7', '9']
    """
    square_0_0 = [
        (0, 0),
        (0, 1),
        (0, 2),
        (1, 0),
        (1, 1),
        (1, 2),
        (2, 0),
        (2, 1),
        (2, 2),
    ]
    square_1_0 = [
        (3, 0),
        (3, 1),
        (3, 2),
        (4, 0),
        (4, 1),
        (4, 2),
        (5, 0),
        (5, 1),
        (5, 2),
    ]
    square_2_0 = [
        (6, 0),
        (6, 1),
        (6, 2),
        (7, 0),
        (7, 1),
        (7, 2),
        (8, 0),
        (8, 1),
        (8, 2),
    ]
    square_0_1 = [
        (0, 3),
        (0, 4),
        (0, 5),
        (1, 3),
        (1, 4),
        (1, 5),
        (2, 3),
        (2, 4),
        (2, 5),
    ]
    square_1_1 = [
        (3, 3),
        (3, 4),
        (3, 5),
        (4, 3),
        (4, 4),
        (4, 5),
        (5, 3),
        (5, 4),
        (5, 5),
    ]
    square_2_1 = [
        (6, 3),
        (6, 4),
        (6, 5),
        (7, 3),
        (7, 4),
        (7, 5),
        (8, 3),
        (8, 4),
        (8, 5),
    ]
    square_0_2 = [
        (0, 6),
        (0, 7),
        (0, 8),
        (1, 6),
        (1, 7),
        (1, 8),
        (2, 6),
        (2, 7),
        (2, 8),
    ]
    square_1_2 = [
        (3, 6),
        (3, 7),
        (3, 8),
        (4, 6),
        (4, 7),
        (4, 8),
        (5, 6),
        (5, 7),
        (5, 8),
    ]
    square_2_2 = [
        (6, 6),
        (6, 7),
        (6, 8),
        (7, 6),
        (7, 7),
        (7, 8),
        (8, 6),
        (8, 7),
        (8, 8),
    ]

    squares = [
        square_0_0,
        square_0_1,
        square_0_2,
        square_1_0,
        square_1_1,
        square_1_2,
        square_2_0,
        square_2_1,
        square_2_2,
    ]
    block_content = []
    for square in squares:
        if pos in square:
            for value in square:
                block_content.append(grid[value[0]][value[1]])
            break

    return block_content


def find_empty_positions(grid: List[List[str]]) -> Optional[Tuple[int, int]]:  # type: ignore[return]
    """Найти первую свободную позицию в пазле

    >>> find_empty_positions([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']])
    (0, 2)
    >>> find_empty_positions([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']])
    (1, 1)
    >>> find_empty_positions([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']])
    (2, 0)
    """
    for row_index in range(len(grid)):
        for column_index in range(len(grid)):
            if grid[row_index][column_index] == ".":
                empty_position = (row_index, column_index)
                return empty_position


def find_possible_values(grid: List[List[str]], pos: Tuple[int, int]) -> Set[str]:  # type: ignore[return]
    """Вернуть множество возможных значения для указанной позиции

    >>> grid = read_sudoku('puzzle1.txt')
    >>> values = find_possible_values(grid, (0,2))
    >>> values == {'1', '2', '4'}
    True
    >>> values = find_possible_values(grid, (4,7))
    >>> values == {'2', '5', '9'}
    True
    """
    range_of_possible_numbers = {"1", "2", "3", "4", "5", "6", "7", "8", "9"}
    already_numbers_in_column = set(get_col(grid, pos))
    already_numbers_in_row = set(get_row(grid, pos))
    already_numbers_in_block = set(get_block(grid, pos))
    possible_numbers_for_cell = (
        range_of_possible_numbers
        - already_numbers_in_column
        - already_numbers_in_row
        - already_numbers_in_block
    )
    return possible_numbers_for_cell


def solve(grid: List[List[str]]) -> Optional[List[List[str]]]:  # type: ignore[return]
    """ Решение пазла, заданного в grid """
    """ Как решать Судоку?
        1. Найти свободную позицию
        2. Найти все возможные значения, которые могут находиться на этой позиции
        3. Для каждого возможного значения:
            3.1. Поместить это значение на эту позицию
            3.2. Продолжить решать оставшуюся часть пазла

    >>> grid = read_sudoku('puzzle1.txt')
    >>> solve(grid)
    [['5', '3', '4', '6', '7', '8', '9', '1', '2'], ['6', '7', '2', '1', '9', '5', '3', '4', '8'], ['1', '9', '8', '3', '4', '2', '5', '6', '7'], ['8', '5', '9', '7', '6', '1', '4', '2', '3'], ['4', '2', '6', '8', '5', '3', '7', '9', '1'], ['7', '1', '3', '9', '2', '4', '8', '5', '6'], ['9', '6', '1', '5', '3', '7', '2', '8', '4'], ['2', '8', '7', '4', '1', '9', '6', '3', '5'], ['3', '4', '5', '2', '8', '6', '1', '7', '9']]
    """
    try:
        pos = find_empty_positions(grid)
        possible_values = find_possible_values(grid, pos)  # type: ignore

        if len(possible_values) == 0:
            pass
        else:
            for possible_value in possible_values:
                edited_grid = [i[:] for i in grid]
                edited_grid[pos[0]][pos[1]] = possible_value  # type: ignore
                answer = solve(edited_grid)
                if answer is not None:
                    return answer
    except Exception as e:
        return grid


def check_solution(solution: List[List[str]]) -> bool:
    """ Если решение solution верно, то вернуть True, в противном случае False """
    # TODO: Add doctests with bad puzzles
    if len(solution) == 9:
        numbers_template = set([str(i) for i in range(1, 9 + 1)])
        for i in range(len(solution)):
            if numbers_template == set(get_col(solution, (0, i))):
                pass
            else:
                return False

        for i in range(len(solution)):
            if numbers_template == set(get_row(solution, (i, 0))):
                pass
            else:
                return False

        for i in range(len(solution)):
            for j in range(len(solution)):
                if numbers_template == set(get_block(solution, (i, j))):
                    pass
                else:
                    return False

        return True
    else:
        return False


def generate_sudoku(N: int) -> List[List[str]]:
    """Генерация судоку заполненного на N элементов

    >>> grid = generate_sudoku(40)
    >>> sum(1 for row in grid for e in row if e == '.')
    41
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(1000)
    >>> sum(1 for row in grid for e in row if e == '.')
    0
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(0)
    >>> sum(1 for row in grid for e in row if e == '.')
    81
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    """
    import random

    n = 3
    table = [
        [str(((i * n + i // n + j) % (n * n) + 1)) for j in range(n * n)]
        for i in range(n * n)
    ]
    for i in range(random.randint(0, 4)):
        table = list(map(list, zip(*table)))

    all_cells_coordinates = [(i, j) for j in range(9) for i in range(9)]
    random.shuffle(all_cells_coordinates)

    if N > 81:
        N = 81

    replace_counter = 0
    while 81 - replace_counter != N:
        coordinates = all_cells_coordinates.pop()
        table[coordinates[0]][coordinates[1]] = "."
        replace_counter += 1

    return table


if __name__ == "__main__":
    for fname in ["puzzle1.txt", "puzzle2.txt", "puzzle3.txt"]:
        grid = read_sudoku(fname)
        display(grid)
        solution = solve(grid)
        if not solution:
            print(f"Puzzle {fname} can't be solved")
        else:
            display(solution)
