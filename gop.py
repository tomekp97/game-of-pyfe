import sys
import random
import time

import pygame

"""
Rules:
    Any live cell with fewer than two live neighbors dies, as if by underpopulation.
    Any live cell with two or three live neighbors lives on to the next generation.
    Any live cell with more than three live neighbors dies, as if by overpopulation.
    Any dead cell with exactly three live neighbors becomes a live cell, as if by reproduction.
"""
FPS = 5

WIDTH = 400
HEIGHT = 400

BLACK = (0, 0, 0)
WHITE = (255,255,255)

CELL_SIZE = int((WIDTH / 100) * 1.5)
GRIDWIDTH = int(WIDTH / CELL_SIZE)
GRIDHEIGHT = int(HEIGHT / CELL_SIZE)
CELL_INDEX_CHANGE = GRIDWIDTH 

MAX_STARTING_CELLS = CELL_SIZE * 22

pygame.init()
surface = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()

class Cell(pygame.Rect):
    def __init__(self, x, y):
        self.alive = False
        self.x = x
        self.y = y
        self.width = CELL_SIZE
        self.height = CELL_SIZE

    def spawn(self):
        if self.alive:
            pygame.draw.rect(surface, WHITE, self, 1)
        else:
            pygame.draw.rect(surface, BLACK, self, 1)
    
def generate_cells():
    cell_map = []

    for y in range(0, WIDTH, CELL_SIZE):
        for x in range(0, HEIGHT, CELL_SIZE):
            cell = Cell(x, y)
            cell_map.append(cell)

    return cell_map

cell_map = generate_cells()

def check_alive_neighbours(array, index):
    neighbours = []
    alive_neighbours = 0

    if array[index].y != 0 and array[index].x != 0:
        n_top_left = array[index  - (CELL_SIZE + 1)]
        neighbours.append(n_top_left)

    if array[index].y != 0:
        n_top = array[index - CELL_SIZE]
        neighbours.append(n_top)

        if array[index].x != 0:
            n_top_left = array[index  - (CELL_SIZE + 1)]
            neighbours.append(n_top_left)
        
        if array[index].x != WIDTH - CELL_SIZE:
            n_top_right = array[index - (CELL_SIZE - 1)]
            neighbours.append(n_top_right)

    if array[index].x != 0:
        n_left = array[index - 1]
        neighbours.append(n_left)

    if array[index].x != WIDTH - CELL_SIZE:
        n_right = array[index - 1]
        neighbours.append(n_right)

    try:
        n_bottom_left = array[index + (CELL_SIZE - 1)]
        if n_bottom_left.x != 0 and n_bottom_left.y != HEIGHT - CELL_SIZE:
            neighbours.append(n_bottom_left)
    except:
        pass

    try:
        n_bottom = array[index + CELL_SIZE]
        if n_bottom.y != HEIGHT - CELL_SIZE:
            neighbours.append(n_bottom)
    except:
        pass

    try:
        n_bottom_right = array[index + (CELL_SIZE + 1)]
        if n_bottom_right.x != WIDTH - CELL_SIZE and n_bottom_right.y != HEIGHT - CELL_SIZE:
            neighbours.append(n_bottom_right)
    except:
        pass

    for n in neighbours:
        if n.alive:
            alive_neighbours += 1

    return alive_neighbours

def generation_spawn():
    starting_cells = 0

    for sc in range(0, MAX_STARTING_CELLS):
        if starting_cells == MAX_STARTING_CELLS:
            break
        
        random_cell_index = random.randrange(len(cell_map))
        cell = cell_map[random_cell_index]
        cell_map[random_cell_index].alive = True
        cell_map[random_cell_index].spawn()

        starting_cells += 1

generation_spawn()

while True:
    clock.tick(FPS)
    generation_spawn()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    surface.fill(BLACK)

    for index in range(0, len(cell_map)):
        cell = cell_map[index]
        alive_neighbours = check_alive_neighbours(cell_map, index)

        if cell.alive and alive_neighbours < 2:
            cell.alive = False

        if cell.alive and (alive_neighbours == 2 or alive_neighbours == 3):
            cell.alive = True
        
        if cell.alive and alive_neighbours > 3:
            cell.alive = False
        
        if not cell.alive and alive_neighbours == 3:
            cell.alive = True

        cell.spawn()

    # time.sleep(0.5)
    pygame.display.update()