import sys
import matplotlib.pyplot as lab
from matplotlib.colors import ListedColormap

def main(file_path: str):
    map = file_reader(file_path)
    map = parse_lab_string(map)
    lab_drawer(map)
    start = map_finder(2, map)
    end = map_finder(5, map)
    loop(start, end, map)
    return 0

def loop(start, end, map_array):
    if start is None:
        print("Points de départ manquant ou invalide !")
        return
    if end is None:
        print("Point d'arrivée invalide ou manquant !")
        return

    path = astar(start, end, map_array)
    if path is None:
        print("Pas de chemin valide trouvé !")
        return

    for current in path:
        map_array[current[0]][current[1]] = 3
        lab_drawer(map_array)
    print("Chemin trouvé !")

def cost(current, neighbour):
    return 1

def astar(start, end, map_array):
    open_list = []
    closed_list = []
    parents = {}
    g_cost = {}
    f_cost = {}

    open_list.append(start)
    g_cost[start] = 0
    f_cost[start] = heuristic(start, end)

    while open_list:
        current = min(open_list, key=lambda x: f_cost[x])
        if current == end:
            return reconstruct_path(parents, end)

        open_list.remove(current)
        closed_list.append(current)

        for neighbour in get_neighbours(current, map_array):
            if neighbour in closed_list:
                continue

            tentative_g_cost = g_cost[current] + cost(current, neighbour)

            if neighbour not in open_list:
                open_list.append(neighbour)
            elif tentative_g_cost >= g_cost[neighbour]:
                continue

            parents[neighbour] = current
            g_cost[neighbour] = tentative_g_cost
            f_cost[neighbour] = tentative_g_cost + heuristic(neighbour, end)

    return None

def reconstruct_path(parents, end):
    path = [end]
    while end in parents:
        end = parents[end]
        path.append(end)
    path.reverse()
    return path

def heuristic(node, goal):
    return abs(node[0] - goal[0]) + abs(node[1] - goal[1])

def get_neighbours(node, map_array):
    rows, cols = len(map_array), len(map_array[0])
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    neighbours = []
    for dx, dy in directions:
        nx, ny = node[0] + dx, node[1] + dy
        if 0 <= nx < rows and 0 <= ny < cols and map_array[nx][ny] != 1:
            neighbours.append((nx, ny))
    return neighbours

def map_finder(unit, map):
    for y, row in enumerate(map):
        for x, cell in enumerate(row):
            if cell == unit:
                return (y, x)
    return None

def lab_drawer(lab_code):
    cmap = ListedColormap(['white', 'black', 'yellow', 'blue', 'yellow', 'red'])
    lab.ion()
    lab.imshow(lab_code, cmap=cmap)
    lab.xticks([])
    lab.yticks([])
    lab.draw()
    lab.pause(0.2)
    lab.clf()

def parse_lab_string(lab_code: str):
    array_2d = []
    lines = lab_code.strip().split("\n")
    for line in lines:
        line = line.strip()
        full_line = [int(char) for char in line]
        array_2d.append(full_line)
    return array_2d

def file_reader(file_path: str):
    with open(file_path, 'r', encoding="utf-8") as open_file:
        content = open_file.read()
    return content

if __name__ == "__main__":
    main(sys.argv[1])
