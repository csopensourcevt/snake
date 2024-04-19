"""
README

Built with
    1. Python 3.8.6
    2. PyGame 2.1.2

Installation
    1. Recommended Python version 3.8.6
    2. PyGame does not support Python version 3.9.0 as of Oct 26, 2020
    3. Install PyGame following https://www.pygame.org/wiki/GettingStarted

How to play
    1. Download file and place it in desired directory
    2. Go to directory in terminal
    3. launch snake.py file in terminal, keeping terminal window
        side-by-side the launched GUI for score tracking
"""


import pygame
import random

pygame.init()


"""
NOTE: __________________________________________________________________________
    * entirely capital variables are constants (no change in values after
        declaration)
    * user may change TICKRATE in the SETUP section below (recommended between
        20 and 60, inclusive)
    * user may change the color values in the COLORS section below
    * user may change BLOCKS_PER_SIDE in the GRID section below (recommended
        between 20 and 40, inclusive)

    *** ALWAYS MOVE/GENERATE SNAKE BEFORE GENERATING FOOD

In the grid,
    0 = unoccupied,     white
    1 = snake head,     dark green
    2 = snake body,     light green
    3 = food,           orange
    4 = wall,           gray
"""

"""
SETUP __________________________________________________________________________
"""
# TICKRATE is updates/second
TICKRATE = 20


"""
COLORS _________________________________________________________________________
"""
UNASSIGNED = (255, 255, 255)      # white
SNAKE_HEAD = (0, 100, 0)          # dark green
SNAKE_BODY = (0, 200, 0)          # light green
FOOD = (200, 100, 0)              # orange
WALL = (50, 50, 50)               # gray
COLOR_LIST = [UNASSIGNED, SNAKE_HEAD, SNAKE_BODY, FOOD, WALL]
BACKGROUND = (0, 0, 0)            # black (not in list above)


"""
GRID ___________________________________________________________________________
"""
BLOCK_SIZE = 20       # in pixels
BLOCK_MARGINS = 1      # in pixels
BLOCKS_PER_SIDE = 30

# constrict grid block margins
if BLOCK_MARGINS != 1:
    BLOCK_MARGINS = 1


# initialize grid walls, walls are '4'
#   * first and last rows are all walls
#   * non-first, non-last rows are walls on the edges, unassigned in the middle
#   EX, BLOCKS_PER_SIDE = 5:
#           4 4 4 4 4
#           4 0 0 0 4
#           4 0 0 0 4
#           4 0 0 0 4
#           4 4 4 4 4
grid = []
grid_first_and_last_rows = [4]*BLOCKS_PER_SIDE
grid_middle_rows = [4]

for i in range(BLOCKS_PER_SIDE-2):
    grid_middle_rows.append(0)
grid_middle_rows.append(4)

grid.append(grid_first_and_last_rows[:])
for i in range(BLOCKS_PER_SIDE-2):
    grid.append(grid_middle_rows[:])
grid.append(grid_first_and_last_rows[:])


"""
SNAKE __________________________________________________________________________
"""
VELOCITY = 1            # standard, unchanging velocity. DO NOT CHANGE FROM 1.
Y = BLOCKS_PER_SIDE // 2   # unchanging initial y position in center of grid y-wise
X = BLOCKS_PER_SIDE // 2   # unchanging initial x position in center of grid x-wise
y_velocity = 0          # initial y velocity = 0, not moving in the y-direction
x_velocity = VELOCITY   # initial x velocity = 1, moving right

def resetSnake():
    # sweeps the current grid for any snake positons, '1' and '2', and
        # unassigns them back to '0'
    for y in range(1, BLOCKS_PER_SIDE - 1):             # not in wall indices
        for x in range(1, BLOCKS_PER_SIDE - 1):         # not in wall indices
            if grid[y][x] in [1, 2]:
                grid[y][x] = 0
    grid[Y][X] = 1
    return [[Y, X]]


# set snake_picture to default [[Y,X]]
snake_picture = resetSnake()  # index 0 = head, other indices = body

# boolean below used for allowing or denying snake from growing
# allow snake to grow if it gets food, deny if it doesn't
delete_last_snake_body = True

"""
FOOD ___________________________________________________________________________
"""
def generateFood():
    # reason is to set food_y and food_x to something not in snake_picture.
    # set food_y and food_x initially to snake head values so that the food_y
        # and food_x values can randomly generate away from the snake_picture
        # values by comparison in the while loop
    food_y, food_x = snake_picture[0][0], snake_picture[0][1]
    while [food_y, food_x] in snake_picture:
        food_y = random.randrange(1, BLOCKS_PER_SIDE - 1)   # not in wall indices
        food_x = random.randrange(1, BLOCKS_PER_SIDE - 1)   # not in wall indices
    return [food_y, food_x]


# set food_picture to a random location not snake head's current location
food_picture = generateFood()


"""
SCORING SYSTEM _________________________________________________________________
"""
attempt = 1         # attempt starts at 1
score = 0           # score starts at 0
highscore = 0       # high score starts at 0
# movesleft = area of playable grid plus an extra 10%
# playable grid means non-wall indices, which is (BLOCKS_PER_SIDE-2)**2
movesleft = int(1.1 * ((BLOCKS_PER_SIDE - 2)**2))
MOVESLEFT_ORIGINAL = movesleft          # unchanging original moves count


"""
PRE-LOOP _______________________________________________________________________
"""
GAME_WINDOW_SIZE = (BLOCK_SIZE + BLOCK_MARGINS) * BLOCKS_PER_SIDE +\
    BLOCK_MARGINS
GAME_WINDOW = pygame.display.set_mode((GAME_WINDOW_SIZE, GAME_WINDOW_SIZE))
CLOCK = pygame.time.Clock()
GAME_WINDOW.fill(BACKGROUND)
print(f"attempt {attempt}, score {score}, high score {highscore}")
running = True


"""
LOOP ___________________________________________________________________________
"""
while running:

    """
    EXIT USING 'X' BUTTON ______________________________________________________
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    """
    KEY PRESS __________________________________________________________________
    """
    # does not allow the snake to 180 its current path
    # can move with arrow keys or w, a, s, d (upper or lowercase)
    action = pygame.key.get_pressed()
    if action[pygame.K_UP] or action[pygame.K_w]:
        reference_x, reference_y = x_velocity, y_velocity
        if y_velocity != VELOCITY:
            x_velocity = 0
            y_velocity = -VELOCITY
    elif action[pygame.K_DOWN] or action[pygame.K_s]:
        reference_x, reference_y = x_velocity, y_velocity
        if y_velocity != -VELOCITY:
            x_velocity = 0
            y_velocity = VELOCITY
    elif action[pygame.K_LEFT] or action[pygame.K_a]:
        reference_x, reference_y = x_velocity, y_velocity
        if x_velocity != VELOCITY:
            x_velocity = -VELOCITY
            y_velocity = 0
    elif action[pygame.K_RIGHT] or action[pygame.K_d]:
        reference_x, reference_y = x_velocity, y_velocity
        if x_velocity != -VELOCITY:
            x_velocity = VELOCITY
            y_velocity = 0

    """
    MODIFY MOVES LEFT __________________________________________________________
    """
    pygame.display.set_caption(
        f"moves left {movesleft} / {MOVESLEFT_ORIGINAL}")
    movesleft -= 1

    """
    COLLISION WITH FOOD ________________________________________________________
        * ONLY TO START THE PROCESS OF ADDING A BODY PART AND RESETTING
            THE FOOD LOCATION. THE PROCESS WILL BE COMPLETED IN THE
            DRAW SNAKE SECTION BELOW.
    """
    # if head location matches food location
    if [snake_picture[0][0], snake_picture[0][1]] == food_picture:
        delete_last_snake_body = False
        score += 1
        movesleft = MOVESLEFT_ORIGINAL
        print(f"attempt {attempt}, score {score}, high score {highscore}")

    """
    COLLISION WITH WALL OR OWN BODY, OR MOVES LEFT = 0 _________________________
    """
    w = False   # wall
    i = False   # itself
    m = False   # moves left

    # hit wall
    if snake_picture[0][0] in [0, BLOCKS_PER_SIDE - 1] or\
            snake_picture[0][1] in [0, BLOCKS_PER_SIDE - 1]:
        w = True
        grid[snake_picture[0][0]][snake_picture[0][1]] = 4
    # hit itself (excluding head)
    if [snake_picture[0][0], snake_picture[0][1]] in snake_picture[1:]:
        i = True
        grid[snake_picture[0][0]][snake_picture[0][1]] = 0
    if movesleft == 0:
        m = True

    if i or w or m:
        # set the food location to unoccupied
        grid[food_picture[0]][food_picture[1]] = 0
        # reset snake to original location, reset velocities to their original
        # values
        snake_picture = resetSnake()
        y_velocity = 0
        x_velocity = VELOCITY
        # reset food to random position
        food_picture = generateFood()
        # update score, highscore, and attempt
        if score > highscore:
            highscore = score
        score = 0
        attempt += 1
        movesleft = MOVESLEFT_ORIGINAL
        # print updated stats
        print(f"attempt {attempt}, score {score}, high score {highscore}")

    """
    DRAW SNAKE _________________________________________________________________
    """
    # snake head after moving
    new_snake_head = [[snake_picture[0][0] + y_velocity, snake_picture[0][1] + x_velocity]]
    grid[snake_picture[len(snake_picture) - 1][0]][snake_picture[len(snake_picture) - 1][1]] = 0

    # if no collision with food
    if delete_last_snake_body:
        # update snake_picture with with previous last element in snake_picture
            # removed
        snake_picture = new_snake_head + snake_picture[:len(snake_picture) - 1]
    # if collision with food
    else:
        # update snake_picture with previous last element in snake_picture
            # present
        snake_picture = new_snake_head + snake_picture
        delete_last_snake_body = True
        # reset food to random position
        food_picture = generateFood()

    """
    DRAW BOARD _________________________________________________________________
    """
    # set head position to 1 so it can be referenced as COLOR_LIST[1]
    grid[snake_picture[0][0]][snake_picture[0][1]] = 1

    # for all other positions in snake_picture, set body position to 2 so it
    # can be referenced as COLOR_LIST[2]
    for index in range(len(snake_picture) - 1):
        grid[snake_picture[index + 1][0]][snake_picture[index + 1][1]] = 2

    # set food position to 3 so it can be referenced as COLOR_LIST[3]
    grid[food_picture[0]][food_picture[1]] = 3

    for y in range(BLOCKS_PER_SIDE):
        for x in range(BLOCKS_PER_SIDE):
            pygame.draw.rect(GAME_WINDOW, COLOR_LIST[grid[y][x]],
                [
                (BLOCK_SIZE + BLOCK_MARGINS) * x + BLOCK_MARGINS,
                (BLOCK_SIZE + BLOCK_MARGINS) * y + BLOCK_MARGINS,
                BLOCK_SIZE,
                BLOCK_SIZE
            ])

    """
    TICK FRAMES/SEC AND FLIP ___________________________________________________
    """
    CLOCK.tick(TICKRATE)
    pygame.display.flip()


"""
QUIT ___________________________________________________________________________
"""
pygame.quit()