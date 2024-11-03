import pygame
import pprint
from queue import Queue

WIDTH  = 800
HEIGHT = 800
FPS = 60

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
quit_game = False

clock = pygame.time.Clock()
dt = 0 # in seconds

# helper to draw square
def draw_square(pos, size, color, outline):
    r = [pos[0], pos[1], size, size]
    pygame.draw.rect(screen, color, r, outline)

class Cell:
    def __init__(self, size):
        self.size  = size

    def draw(self, i, j):
        r = pygame.Rect(i*self.size[0], j*self.size[1], self.size[0], self.size[1])
        border = 1
        pygame.draw.rect(screen, "white", r, border)

CELL_SIZE = 16
assert WIDTH % CELL_SIZE == 0, f"CELL_SIZE {CELL_SIZE} is not divisble by WIDTH {WIDTH}!"
assert HEIGHT % CELL_SIZE == 0, f"CELL_SIZE {CELL_SIZE} is not divisble by HEIGHT {HEIGHT}!"
COLS = int(WIDTH / CELL_SIZE)
ROWS = int(HEIGHT / CELL_SIZE)
# print(f"COLS: {COLS}")
# print(f"ROWS: {ROWS}")
# pprint.pp(len(grid))
# pprint.pp(len(grid[0]))

cell = Cell((CELL_SIZE, CELL_SIZE))
grid = []
path = []
flow_chart = []
walls = {}

prev_mouse_state = [False, False, False]
mouse_pressed =    [False, False, False]
mouse_released =   [False, False, False]
LEFT = 0
MIDDLE = 1
RIGHT = 2

prev_start_set_key_state = False
prev_end_set_key_state   = False

start_set_key_state_pressed = False
end_set_key_state_pressed   = False

# start_index = (None, None)
start_index = (0, 10)
end_index =   (None, None)

def clamp(value, mi, ma):
    return min(ma, max(value, mi))

for r in range(ROWS):
    row = []
    for c in range(COLS):
        row.append(Cell((CELL_SIZE, CELL_SIZE)))
    grid.append(row)

def get_cell_nbors(i, j):
    nbors = []
    directions = [ (-1,  0), ( 1,  0),
                   ( 0, -1), ( 0,  1),
                   (-1, -1), (-1,  1),
                   ( 1, -1), ( 1,  1) ]

    for di, dj in directions:
        ni = i + di
        nj = j + dj
        # Check if the neighbor is within bounds
        if 0 <= ni < ROWS and 0 <= nj < COLS:
            nbors.append((ni, nj))
    return nbors

# Returns flow-chart to start from every cell
def a_star(grid, start, end):
    # frontier = [start]
    frontier = Queue()
    frontier.put(start)
    came_from = dict()
    came_from[start] = None

    # pprint.pp(f"Starting from {start}")
    while not frontier.empty():
        current = frontier.get()
        if current in walls and walls[current]:
            continue
        if current == end:
            break
        for n in get_cell_nbors(current[0], current[1]):
            if n not in came_from:
                frontier.put(n)
                came_from[n] = current
                # pprint.pp(f"Reached from {n}")

    # assert len(came_from) == COLS*ROWS, "Couldn't calculate flow-chart of every cell!"
    return came_from

def reconstruct_path(grid, flow_chart, start, end):
    current = end
    path = []
    while current != start:
        try:
            current = flow_chart[current]
        except Exception as e:
            return path
        path.append(current)
    # pprint.pp(f"Calculated path! of {len(path)} cells")
    return path

def is_start_end_ready():
    return end_index[0] != None and end_index[1] != None and end_index[0] != None and end_index[1] != None

while not quit_game:
    # Mouse press/release
    mouse_state = pygame.mouse.get_pressed()
    mouse_pressed = list(map(lambda x: True if not prev_mouse_state[x[0]] and x[1] else False, enumerate(mouse_state)))
    mouse_released = list(map(lambda x: True if prev_mouse_state[x[0]] and not x[1] else False, enumerate(mouse_state)))
    prev_mouse_state = mouse_state

    # Key press
    start_set_key_state = pygame.key.get_pressed()[pygame.K_z]
    start_set_key_state_pressed = not prev_start_set_key_state and start_set_key_state
    prev_start_set_key_state = start_set_key_state

    end_set_key_state = pygame.key.get_pressed()[pygame.K_x]
    end_set_key_state_pressed = not prev_end_set_key_state and end_set_key_state
    prev_end_set_key_state = end_set_key_state

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit_game = True
    screen.fill("black")

    # Set/Reset wall on mouse hold
    mpos = pygame.mouse.get_pos()
    mi, mj = int(mpos[0] / CELL_SIZE), int(mpos[1] / CELL_SIZE)
    hovering_cell = grid[mi][mj]
    # hovering_cell.on = True
    pygame.draw.circle(screen, "red", (mi*CELL_SIZE + CELL_SIZE*0.5, mj*CELL_SIZE + CELL_SIZE*0.5), CELL_SIZE/8)

    if mouse_state[LEFT]:
        walls[(mi, mj)] = True
    if mouse_state[RIGHT]:
        walls[(mi, mj)] = False

    #     for n in get_cell_nbors(mi, mj):
    #         grid[n[0]][n[1]].color = "red"

    # Set start and end
    if start_set_key_state_pressed:
        start_index = (mi, mj)
    if end_set_key_state_pressed:
        end_index = (mi, mj)

    # TODO: Can check if the clicking index is not the current start/end index and not calculate path
    if mouse_state[LEFT] or mouse_state[RIGHT] or start_set_key_state_pressed or end_set_key_state_pressed:
        if is_start_end_ready():
            flow_chart = a_star(grid, start_index, end_index)
            path = reconstruct_path(grid, flow_chart, start_index, end_index)
        # pprint.pp(path)

    # Draw grid
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            cell.draw(i, j)
            cell.on = False

    k = 10
    # Draw flow-chart
    for p in flow_chart:
        draw_square((p[0]*CELL_SIZE, p[1]*CELL_SIZE), CELL_SIZE-2, (k, k, k, 255), 0)

    # Highlight the cells in path
    for p in path:
        draw_square((p[0]*CELL_SIZE, p[1]*CELL_SIZE), CELL_SIZE-2, "yellow", 0)

    # Draw walls
    for p in walls:
        if not walls[p]: continue
        draw_square((p[0]*CELL_SIZE, p[1]*CELL_SIZE), CELL_SIZE-2, "gray", 0)

    # Draw start and end
    if start_index[0] != None and start_index[1] != None:
        draw_square((start_index[0]*CELL_SIZE, start_index[1]*CELL_SIZE), CELL_SIZE, "green", 0)

    if end_index[0] != None and end_index[1] != None:
        draw_square((end_index[0]*CELL_SIZE, end_index[1]*CELL_SIZE), CELL_SIZE, "blue", 0)

    pygame.display.flip()

    dt = clock.tick(FPS) / 1000.0

pygame.quit()
