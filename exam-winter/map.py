def main():
    path_to_map = input()
    start_map = read(path_to_map)

    updated_map = create_rout(start_map)

    print(updated_map)


def read(path_to_map):
    # 1. считывание

    initial_map_file = []

    with open(path_to_map, encoding="utf-8") as initial_map_file:
        initial_map_file = initial_map_file.read().splitlines()
    for i in range(0, len(initial_map_file)):
        initial_map_file[i] = list(initial_map_file[i])

    return initial_map_file


def create_rout(current_map):

    for i in range(0, len(current_map)):
        for j in range(0, len(current_map[i])):
            if current_map[i][j] == ".":
                current_map[i][j] = "☺"
    return current_map


if __name__ == "__main__":
    main()




