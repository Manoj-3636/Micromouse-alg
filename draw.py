import turtle
from fnmatch import translate

import maze_solver
# (bottom,right,top,left)
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

size_x = 100
size_y = 100
path = maze_solver.find_path()
def main():
    convert_maze()
    # print(sample_maze)
    draw()


def convert_maze():
    for row in sample_maze:
        for column_index in range(len(row)):
            row[column_index] = square_types[row[column_index]]

def draw():
    # Init
    side = len(sample_maze) * 100
    # Assuming the maze is a square as in the rules its written that
    # The maze is composed of multiples of an 18 cm x 18 cm unit square
    #  The maze comprises up to 16 x 16 unit squares

    global wn
    wn = turtle.Screen()
    wn.setup(side+100,side+100)
    wn.bgcolor("black")
    wn.title("Maze")

    global pen
    pen = turtle.Turtle()
    pen.color("white")
    pen.speed(0)

    to_corner(side)
    draw_box(side)
    draw_horizontal(100,side)
    draw_vertical(100,side)
    draw_path(100,side)
    turtle.done()

def to_corner(side):
    pen.penup()
    pen.setx(-side/2)
    pen.sety(-side/2)
    pen.pendown()

# Angle is taken wrt to positive x axis -> Anticlockwise is positive only positive values are allowed
def set_angle(angle:float) -> None:
    current_angle = pen.heading()
    if angle>current_angle :
        pen.left(angle-current_angle)

    elif angle<current_angle:
        pen.right(current_angle - angle)

def draw_box(side):
    for x in range (4):
        pen.forward(side)
        pen.left(90)

def draw_horizontal(side_unit,side):
    translated_coord = side/2
    for row_index in range(len(sample_maze)):
        pen.penup()
        pen.goto(-translated_coord,translated_coord-((row_index)*100))
        # pen.setx(translated_coord)
        # pen.sety(translated_coord + (row_index * 100))

        pen.pendown()

        for cell in sample_maze[row_index]:
            bottom_bool = bool(cell[2])
            if bottom_bool:
                pen.pendown()
            else:
                pen.penup()

            pen.forward(side_unit)

    pen.pendown()


def compile_cells_data(column_index:int):
    compiled_data = []

    # since column index starts from 0 we take every row and get information of the column index's wall boolean
    for row in sample_maze:
        cell = row[column_index]
        compiled_data.append(cell[-1])

    return compiled_data

def draw_vertical(side_unit,side):
    translated_coord = side/2
    for column_index in range(len(sample_maze)):
        pen.penup()

        # this translates the pen to the bottom line and the point where the vertical line intersects bottom
        pen.goto(-translated_coord + (column_index * 100), translated_coord)
        set_angle(270)

        # this compiled the data of the left side bools of a given column

        cells_data = compile_cells_data(column_index)

        for cell in cells_data:
            if bool(cell):
                pen.pendown()
            else:
                pen.penup()

            pen.forward(side_unit)

def draw_path(side_unit,side):
    translated_coord = -side/2 + side_unit/2
    pen.penup()
    pen.goto(translated_coord,translated_coord)
    pen.color("red")
    pen.pensize(3)
    pen.speed(1)
    pen.pendown()
    for coordinate in path:
        x = coordinate[0]
        y = coordinate[1]
        pen.goto(translated_coord+(y*side_unit),translated_coord+(x*side_unit))

if __name__ == "__main__":
    main()