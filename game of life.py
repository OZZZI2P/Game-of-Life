import time
import os
import random
import sys


def clear_console():

    if sys.platform.startswith('win'):
        os.system("cls")
    elif sys.platform.startswith('linux'):
        os.system("clear")
    elif sys.platform.startswith('darwin'):
        os.system("clear")
    else:
        print("Unable to clear terminal. Your operating system is not supported.\n\r")


def resize_console(rows, cols):

    if cols < 32:
        cols = 32

    if sys.platform.startswith('win'):
        command = "mode con: cols={0} lines={1}".format(cols + cols, rows + 5)
        os.system(command)
    elif sys.platform.startswith('linux'):
        command = "\x1b[8;{rows};{cols}t".format(rows=rows + 3, cols=cols + cols)
        sys.stdout.write(command)
    elif sys.platform.startswith('darwin'):
        command = "\x1b[8;{rows};{cols}t".format(rows=rows + 3, cols=cols + cols)
        sys.stdout.write(command)
    else:
        print("Unable to resize terminal. Your operating system is not supported.\n\r")


def create_init_grid(rows, cols):
  

    grid = []
    for row in range(rows):
        grid_rows = []
        for col in range(cols):
            if random.randint(0, 7) == 0:
                grid_rows += [1]
            else:
                grid_rows += [0]
        grid += [grid_rows]
    return grid


def print_grid(rows, cols, grid, generation):

    clear_console()

    output_str = ""

    output_str += "Generation {0} - To exit the program press <Ctrl-C>\n\r".format(generation)
    for row in range(rows):
        for col in range(cols):
            if grid[row][col] == 0:
                output_str += ". "
            else:
                output_str += "* "
        output_str += "\n\r"
    print(output_str, end=" ")


def nextPattern(rows, cols, grid, next_grid):

    for row in range(rows):
        for col in range(cols):
            live_neighbors = neighbourSum(row, col, rows, cols, grid)

            if live_neighbors < 2 or live_neighbors > 3:
                next_grid[row][col] = 0
            elif live_neighbors == 3 and grid[row][col] == 0:
                next_grid[row][col] = 1
            else:
                next_grid[row][col] = grid[row][col]


def neighbourSum(row, col, rows, cols, grid):


    life_sum = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if not (i == 0 and j == 0):
                life_sum += grid[((row + i) % rows)][((col + j) % cols)]
    return life_sum


def grid_changing(rows, cols, grid, next_grid):

    for row in range(rows):
        for col in range(cols):
            if not grid[row][col] == next_grid[row][col]:
                return True
    return False


def get_integer_value(prompt, low, high):


    while True:
        try:
            value = int(input(prompt))
        except ValueError:
            print("Input was not a valid integer value.")
            continue
        if value < low or value > high:
            print("Input was not inside the bounds (value <= {0} or value >= {1}).".format(low, high))
        else:
            break
    return value


def run_game():

    clear_console()

    rows = get_integer_value("Enter the number of rows (10-60): ", 10, 60)
    clear_console()
    cols = get_integer_value("Enter the number of cols (10-118): ", 10, 118)

    generations = 5000
    resize_console(rows, cols)

    current_generation = create_init_grid(rows, cols)
    next_generation = create_init_grid(rows, cols)

    gen = 1
    for gen in range(1, generations + 1):
        if not grid_changing(rows, cols, current_generation, next_generation):
            break
        print_grid(rows, cols, current_generation, gen)
        nextPattern(rows, cols, current_generation, next_generation)
        time.sleep(1 / 5.0)
        current_generation, next_generation = next_generation, current_generation

    print_grid(rows, cols, current_generation, gen)
    return input("<Enter> to exit or r to run again: ")


run = "r"
while run == "r":
    out = run_game()
    run = out