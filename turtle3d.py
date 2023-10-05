import turtle
import numpy as np
import math
import time

t = turtle.Turtle()
t.speed(0)

focal_length = 1000.0
distance_to_screen = 10


# project a 3d point to a 2d point on the screen
def project_point(point):
    x, y, z = point
    scale = focal_length / (focal_length + z)
    screenX = x * scale
    screenY = y * scale
    return (screenX, screenY)

def rotate_x(point, angle):
    matrix = np.array([
        [1, 0, 0],
        [0, math.cos(angle), -math.sin(angle)],
        [0, math.sin(angle), math.cos(angle)]
    ], dtype=np.float32)
    point = np.array(point, dtype=np.float32)
    return tuple(np.matmul(point, matrix))

def rotate_y(point, angle):
    matrix = np.array([
        [math.cos(angle), 0, math.sin(angle)],
        [0, 1, 0],
        [-math.sin(angle), 0, math.cos(angle)]
    ], dtype=np.float32)
    point = np.array(point, dtype=np.float32)
    return tuple(np.matmul(point, matrix))

def cube(x, y, z, a):
    cube = [
        (x, y, z),
        (x + a, y, z),
        (x + a, y + a, z),
        (x, y + a, z),
        (x, y, z + a),
        (x + a, y, z + a),
        (x + a, y + a, z + a),
        (x, y + a, z + a)
    ]
    edges_i = [
        (1, 2),
        (2, 3),
        (3, 4),
        (4, 1),
        (1, 5),
        (2, 6),
        (3, 7),
        (4, 8),
        (5, 6),
        (6, 7),
        (7, 8),
        (8, 5)
    ]
    
    return [(cube[e[0], e[1]]) for e in edges_i]


# draw a cube on the canvas, given the x, y, z of the bottom left front point and the side length
def draw_cube(x, y, z, a, rotX, rotY):
    cube = [
        (x, y, z),
        (x + a, y, z),
        (x + a, y + a, z),
        (x, y + a, z),
        (x, y, z + a),
        (x + a, y, z + a),
        (x + a, y + a, z + a),
        (x, y + a, z + a)
    ]
    edges = [
        (1, 2),
        (2, 3),
        (3, 4),
        (4, 1),
        (1, 5),
        (2, 6),
        (3, 7),
        (4, 8),
        (5, 6),
        (6, 7),
        (7, 8),
        (8, 5)
    ]
    for i in range(len(cube)):
        cube[i] = rotate_y(rotate_x(cube[i], rotX), rotY)
        
        #rotate_x(cube[i], math.pi/4)
    cube_2d = []
    for i in range(len(cube)):
        cube_2d.append((project_point(cube[i])))

    for e in edges:
        t.penup()
        t.goto(cube_2d[e[0]-1])
        t.pendown()
        t.goto(cube_2d[e[1]-1])

# draw a pyramid on the canvas, given the x, y, z of the bottom left front point and the side length
def draw_pyramid(x, y, z, a, rotX, rotY):
    points = [
        (x, y, z),
        (x + a, y, z),
        (x + a, y, z + a),
        (x, y, z + a),
        (x + a/2, y + a, z + a/2)
    ]
    edges = [
        (1, 2),
        (2, 3),
        (3, 4),
        (4, 1),
        (1, 5),
        (2, 5),
        (3, 5),
        (4, 5)
    ]
    for i in range(len(points)):
        points[i] = rotate_y(rotate_x(points[i], rotX), rotY)
        
        #rotate_x(cube[i], math.pi/4)
    cube_2d = []
    for i in range(len(points)):
        cube_2d.append((project_point(points[i])))

    for e in edges:
        t.penup()
        t.goto(cube_2d[e[0]-1])
        t.pendown()
        t.goto(cube_2d[e[1]-1])

def draw_x():
    p1 = (-500, 0 ,0)
    p2 = (500, 0, 0)
    t.color("red")
    t.penup()
    t.goto(project_point(p1))
    t.pendown()
    t.goto(project_point(p2))
    t.color(0,0,0)

def draw_y():
    p1 = (0, 500 ,0)
    p2 = (0, -500, 0)
    t.color("green")
    t.penup()
    t.goto(project_point(p1))
    t.pendown()
    t.goto(project_point(p2))
    t.color(0,0,0)

rotX = 0
rotY = 0
while True:
    draw_x()
    draw_y()
    draw_pyramid(-100, -100, -100, 200, rotX, rotY)
    rotX += 0.2
    rotY += 0.2
    time.sleep(0.01)
    t.clear()
    



turtle.done()