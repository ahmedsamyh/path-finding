import pygame
import pprint

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
        self.size = size
        self.wall = False

    def draw(self, i, j):
        r = pygame.Rect(i*self.size[0], j*self.size[1], self.size[0], self.size[1])
        color = "gray" if self.wall else "white"
        pygame.draw.rect(screen, color, r, 0 if self.wall else 1)

CELL_SIZE = 32
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

for r in range(ROWS):
    row = []
    for c in range(COLS):
        row.append(Cell((CELL_SIZE, CELL_SIZE)))
    grid.append(row)

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
        hovering_cell.wall = True
    if mouse_state[RIGHT]:
        hovering_cell.wall = False

    # Set start and end
    if start_set_key_state_pressed:
        start_index = (mi, mj)
    if end_set_key_state_pressed:
        end_index = (mi, mj)

    # Draw grid
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            cell.draw(i, j)

    # Draw start and end
    if start_index[0] != None and start_index[1] != None:
        draw_square((start_index[0]*CELL_SIZE, start_index[1]*CELL_SIZE), CELL_SIZE, "green", 0)

    if end_index[0] != None and end_index[1] != None:
        draw_square((end_index[0]*CELL_SIZE, end_index[1]*CELL_SIZE), CELL_SIZE, "blue", 0)

    pygame.display.flip()

    dt = clock.tick(FPS) / 1000.0

pygame.quit()
