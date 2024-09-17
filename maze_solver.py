# (bottom,right,top,left)
import json

square_types = {
    1:[0,0,0,1],
    2:[0,0,1,0],
    3:[0,1,0,0],
    4:[1,0,0,0],
    5:[1,0,0,1],
    6:[1,1,0,0],
    7:[0,1,1,0],
    8:[0,0,1,1],
    9:[0,1,0,1],
    10:[1,0,1,0],
    11:[1,1,0,1],
    12:[1,1,1,0],
    13:[0,1,1,1],
    14:[1,0,1,1],
    15:[0,0,0,0],
    16:[1,1,1,1],
}

sample_maze = [[14, 10, 7, 8, 10, 7],
               [8, 12, 9, 11, 13, 9],
               [1, 12, 1, 10, 4, 6],
               [5, 2, 4, 10, 7, 13],
               [13, 9, 14, 2, 6, 9],
               [5, 6, 14, 4, 10, 6]]

discorvered_maze = {}

size = 6
start = (0,0)
goal=(4,3)
fill_dict = {}

def main():
    path = find_path()
    print(path)

def convert_maze():
    for row in sample_maze:
        for column_index in range(len(row)):
            row[column_index] = square_types[row[column_index]]

# All the functions must call this function to get access to current cell data
# This is done to simulate something like an infrared sensor which is on all 4 directions and can tell if there is a
# wall in any direction
def get_current_cell_data(cell_coords):
    if(cell_coords != current_cell):
        print("Asking for data of a cell which is not the current Cell")
    x = cell_coords[0]
    y = cell_coords[1]
    current_row = sample_maze[5-x]
    return current_row[y]

def initial_flood_fill() :
    # Set the goal to floodfill 0 that is the lowest possible level to which water will flow
    fill_dict[goal] = 0

    que = [goal]

    while bool(que):
        parent = que[0]
        # takes members from the que and creates a new maze which serves as the data which the mouse has
        discorvered_maze[parent] = [0,0,0,0]
        neighbours = get_neighbours(parent)

        if neighbours is []:
            del que[0]
            continue
        for neighbour in range(len(neighbours)):
            fill_dict[neighbours[neighbour]] = fill_dict[parent] + 1
            que.append(neighbours[neighbour])
        del que[0]
        # i = i+1

    # print(i)
# Gets blank neighbours cannot be used while updating mostly
def get_neighbours(coordinates):
    x = coordinates[0]
    y = coordinates[1]
    neighbours = [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]
    final_neighbours = []
    for neighbour in range(len(neighbours)):
        coordinates_child = neighbours[neighbour]
        does_it_exist = coordinates_child in fill_dict.keys()

        if not (does_it_exist or ((coordinates_child[0] > 5) or (coordinates_child[1] > 5) or (coordinates_child[0]<0) or (coordinates_child[1] < 0))):
            final_neighbours.append(coordinates_child)
            # print(f"{coordinates_child} is appended in neighbours thru 1")

    # print(final_neighbours)
    # print("_"*100)
    return final_neighbours


def get_accessible_neighbours(cell_data,coords):
    accessible_neighbours = []
    if(cell_data[0] == 0) and (coords[0] - 1 >= 0):
        accessible_neighbours.append((coords[0] - 1,coords[1]))

    if(cell_data[1] == 0 ) and (coords[1]+1 <= 5):
        accessible_neighbours.append((coords[0],coords[1]+1))

    if(cell_data[2] == 0 ) and (coords[0] + 1 <= 5):
        accessible_neighbours.append((coords[0] + 1 , coords[1]))

    if(cell_data[3] == 0) and (coords[1] - 1 >= 0):
        accessible_neighbours.append((coords[0],coords[1] - 1))


    return accessible_neighbours


def get_dist_list(accessible_neighbours):
    dist_list = []
    for neighbour in accessible_neighbours:
        dist_list.append(fill_dict[neighbour])

    return dist_list


def find_path():
    convert_maze()
    initial_flood_fill()
    global current_cell
    current_cell = start
    discorvered_maze[current_cell] = get_current_cell_data(current_cell)
    stack = []
    path = [start]

    # This is going to be the path solving loop
    while current_cell != goal:
        stack.append(current_cell)
        while len(stack) != 0:
            to_be_processed = stack[0]
            del stack[0]
            # to_be_processed = stack.pop()
            accessible_neighbours = get_accessible_neighbours(discorvered_maze[to_be_processed],to_be_processed)

            dist_list = get_dist_list(accessible_neighbours)
            md = min(dist_list)
            cd = fill_dict[to_be_processed]

            if md != (cd - 1):
                fill_dict[to_be_processed] = md + 1
                for accessible_neighbour in accessible_neighbours:
                    stack.append(accessible_neighbour)

        accessible_neighbours = get_accessible_neighbours(discorvered_maze[current_cell],current_cell)
        updated_dist_list = get_dist_list(accessible_neighbours)
        minimum = min(updated_dist_list)
        next_cell = None

        for neighbour in accessible_neighbours:
            if fill_dict[neighbour] == minimum:
                next_cell = neighbour
                break

        current_cell = next_cell
        discorvered_maze[current_cell] = get_current_cell_data(current_cell)
        path.append(next_cell)

    return path


if __name__ == "__main__":
    main()