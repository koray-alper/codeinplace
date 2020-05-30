"""
File: brickbreaker.py
----------------
YOUR DESCRIPTION HERE
"""

import tkinter
import time
import random
import math
# How big is the playing area?
CANVAS_WIDTH = 600      # Width of drawing canvas in pixels
CANVAS_HEIGHT = 750     # Height of drawing canvas in pixels

# Constants for the bricks
N_ROWS = 8              # How many rows of bricks are there?
N_COLS = 10             # How many columns of bricks are there?
SPACING = 5             # How much space is there between each brick?
BRICK_START_Y = 50      # The y coordinate of the top-most brick
BRICK_HEIGHT = 20       # How many pixels high is each brick
BRICK_WIDTH = (CANVAS_WIDTH - (N_COLS+1) * SPACING ) / N_COLS

# Constants for the ball and paddle
BALL_SIZE = 40
PADDLE_Y = CANVAS_HEIGHT - 40
PADDLE_WIDTH = 100
distance = 0
def main():
    # assign the created objects to variables
    canvas = make_canvas(CANVAS_WIDTH, CANVAS_HEIGHT, 'Brick Breaker')
    place_bricks(canvas,SPACING,N_ROWS,N_COLS,BRICK_START_Y)
    ball=insert_ball(canvas, CANVAS_WIDTH, CANVAS_HEIGHT, BALL_SIZE)
    paddle = insert_paddle(canvas, CANVAS_HEIGHT, CANVAS_WIDTH, PADDLE_WIDTH)
    # initial speed of the ball avoids zero speed along x-dimension
    input('press any number to continue: ')
    v_x_0 = 1*random.randint(-2,2)
    v_y_0 = 4
    zz = 82 # index of paddle in canvas
    mouse_x = canvas.winfo_pointerx()
    n_bricks = 80
    failure = 0   # how many times ball fell past paddle.
    stop_game = True  # conditions to end the game satisfied? (3 failure or no bricks)
    temp = 0  # number of incidence that paddle appeared in colliding_list consecutively
    angle_x_axis = 1
    speed=1
    while stop_game:
        # making paddle follow pointer moves
        if canvas.winfo_pointerx() >= PADDLE_WIDTH/2 and canvas.winfo_pointerx() <= (CANVAS_WIDTH - PADDLE_WIDTH / 2):
            mouse_x = canvas.winfo_pointerx()
        elif canvas.winfo_pointerx() < PADDLE_WIDTH/2:
            mouse_x = PADDLE_WIDTH/2
        elif canvas.winfo_pointerx() > (CANVAS_WIDTH - PADDLE_WIDTH/2):
            mouse_x = (CANVAS_WIDTH - PADDLE_WIDTH/2)
        change_x = mouse_x - get_left_x(canvas,paddle) - PADDLE_WIDTH/2
        canvas.move(paddle, change_x, 0)
        # roll the ball, record ball coordinates and pass to colliding_list method
        canvas.move(ball, v_x_0, v_y_0)
        ball_coords = canvas.coords(ball)
        colliding_list = canvas.find_overlapping(ball_coords[0], ball_coords[1], ball_coords[2], ball_coords[3])
        paddle_coords = canvas.coords(paddle)
        # distance between the center of the ball and the paddle
        distance = balls_colliding(ball_coords, paddle_coords)
        speed = math.sqrt(v_x_0*v_x_0 + v_y_0*v_y_0)
        # ball bounces off the side walls of the canvas
        if get_left_x(canvas, ball) <= 0 or get_left_x(canvas, ball) >= CANVAS_WIDTH - BALL_SIZE:
            v_x_0 = -1 * v_x_0
            temp = 0
        # ball bounces up and down as it bumps into paddle canvas x-axis and bricks, and bricks deleted whne hit by wall
        if get_top_y(canvas,ball) <= 0:
            v_y_0 = -1 * v_y_0
            temp = 0
        elif len(colliding_list) > 1 and (not zz in colliding_list):
            for i in range(len(colliding_list)-1):
                canvas.delete(colliding_list[i])
            n_bricks = n_bricks - (len(colliding_list)-1)
            v_y_0 = -1 * v_y_0
            temp = 0
        elif distance <= (BALL_SIZE/2 + PADDLE_WIDTH/2):
            angle_x_axis = angles(v_y_0, v_x_0, ball_coords, paddle_coords)
            temp += 1
            if temp < 2:
                v_x_0 = math.cos(math.radians(angle_x_axis))*speed
                v_y_0 = -1 * math.sin(math.radians(angle_x_axis))*speed
                # MAYBE ADD PADDLE SPEED
        if get_top_y(canvas,ball) > CANVAS_HEIGHT:
            failure += 1
            temp=0
            canvas.move(ball, CANVAS_WIDTH/2 - ball_coords[0] - BALL_SIZE/2, -1*(CANVAS_HEIGHT/2 + BALL_SIZE/2))
            if failure < 3:
                input("press any number to continue: ")
            v_x_0 = 2 * random.randint(-2, 2)
            if v_x_0 == 0:
                v_x_0 = 1
            v_y_0 = 5

        canvas.update()
        time.sleep(1 / 50)
        stop_game = failure < 3 and n_bricks > 0

    if n_bricks==0:
        canvas.create_text(CANVAS_WIDTH/2-50, CANVAS_HEIGHT/2, font=("Purisa", 16), text='Congratulations! You won!')
    elif failure == 3:
        canvas.create_text(CANVAS_WIDTH/2-100, CANVAS_HEIGHT/2, font=("Purisa", 16), text='Game Over!')

    canvas.mainloop()

def get_top_y(canvas, object):
    '''
    This friendly method returns the y coordinate of the top of an object.
    Recall that canvas.coords(object) returns a list of the object
    bounding box: [x_1, y_1, x_2, y_2]. The element at index 1 is the top-y
    '''
    return canvas.coords(object)[1]

def get_left_x(canvas, object):
    '''
    This friendly method returns the x coordinate of the left of an object.
    Recall that canvas.coords(object) returns a list of the object
    bounding box: [x_1, y_1, x_2, y_2]. The element at index 0 is the left-x
    '''
    return canvas.coords(object)[0]

def place_bricks(canvas,SPACING,N_ROWS,N_COLS,BRICK_START_Y):
    colours=['red', 'red', 'orange', 'orange', 'yellow', 'yellow', 'green', 'green', 'cyan', 'cyan']
    for j in range(N_ROWS):
        y_0 = BRICK_START_Y
        y_brick = y_0 + j * (SPACING + BRICK_HEIGHT)
        for i in range(N_COLS):
            x_0 = 5
            x_brick = x_0 + i * (SPACING + BRICK_WIDTH)
            canvas.create_rectangle(x_brick, y_brick, x_brick + BRICK_WIDTH, y_brick + BRICK_HEIGHT, fill=colours[j])


def insert_ball(canvas, CANVAS_WIDTH, CANVAS_HEIGHT, BALL_SIZE):
    x_0 = CANVAS_WIDTH/2 - BALL_SIZE/2
    y_0 = CANVAS_HEIGHT/2 - BALL_SIZE/2
    bounce_ball = canvas.create_oval(x_0, y_0, x_0+ BALL_SIZE, y_0 + BALL_SIZE, fill='black')
    return bounce_ball

def insert_paddle(canvas, CANVAS_HEIGHT, CANVAS_WIDTH, PADDLE_WIDTH):
    #paddle = canvas.create_rectangle(0, PADDLE_Y, PADDLE_WIDTH,PADDLE_Y+10, fill='red')
    x_0 = CANVAS_WIDTH / 2 - PADDLE_WIDTH / 2
    y_0 = CANVAS_HEIGHT - PADDLE_WIDTH / 2
    paddle = canvas.create_oval(x_0, y_0, x_0 + PADDLE_WIDTH, y_0 + PADDLE_WIDTH, fill='red')
    return paddle
#calculates the distance between the center of the ball and the paddle, to catch a collision
def balls_colliding(ball_coords, paddle_coords):
    ball_center_x = (ball_coords[0]+ball_coords[2])/2
    ball_center_y = (ball_coords[1]+ball_coords[3])/2
    paddle_center_x = (paddle_coords[0]+paddle_coords[2])/2
    paddle_center_y = (paddle_coords[1] + paddle_coords[3]) / 2
    distance = math.sqrt(math.pow((ball_center_y - paddle_center_y),2)+ math.pow((paddle_center_x - ball_center_x),2))
    return distance

# calculates the angle of the direction of the ball after hitting to the paddle.
def angles(v_y_0, v_x_0, ball_coords, paddle_coords):
    ball_center_x = (ball_coords[0]+ball_coords[2])/2
    ball_center_y = (ball_coords[1]+ball_coords[3])/2
    paddle_center_x = (paddle_coords[0]+paddle_coords[2])/2
    paddle_center_y = (paddle_coords[1] + paddle_coords[3]) / 2
    m = (paddle_center_y - ball_center_y)/ ( ball_center_x - paddle_center_x)
    if  v_x_0 < 0:
        angle_speed = math.degrees(math.atan(v_y_0 / (-1*v_x_0)))
    elif v_x_0 == 0:
        angle_speed = 90
    else:
        angle_speed = 180 + math.degrees(math.atan(v_y_0 / (-1*v_x_0)))
    if math.degrees(math.atan(-1 / m)) > 0:
        angle_plane = math.degrees(math.atan(-1 / m))
    else:
        angle_plane = 180 + math.degrees(math.atan(-1 / m))
    angle_dif = angle_plane - angle_speed
    angle_x_axis = 180 + angle_plane + angle_dif
    return angle_x_axis


def make_canvas(width, height, title):
    """
    DO NOT MODIFY
    Creates and returns a drawing canvas
    of the given int size with a blue border,
    ready for drawing.
    """
    top = tkinter.Tk()
    top.minsize(width=width, height=height)
    top.title(title)
    canvas = tkinter.Canvas(top, width=width + 1, height=height + 1)
    canvas.pack()
    return canvas

if __name__ == '__main__':
    main()
