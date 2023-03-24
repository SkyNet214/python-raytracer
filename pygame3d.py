import pygame as pg
import numpy as np
import math
import time

WIDTH, HEIGHT = (800, 800)

pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()

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

def rotate_z(point, angle):
    matrix = np.array([
        [math.cos(angle), -math.sin(angle), 0],
        [math.sin(angle), math.cos(angle), 0],
        [0, 0, 1]
    ], dtype=np.float32)
    point = np.array(point, dtype=np.float32)
    return tuple(np.matmul(point, matrix))
# draw a cube on the canvas, given the x, y, z of the bottom left front point and the side length
def draw_cube(x, y, z, a, rotX, rotY, rotZ):
    #x = x + WIDTH / 2
    #y = y - HEIGHT / 2
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
        cube[i] = rotate_z(rotate_y(rotate_x(cube[i], rotX), rotY), rotZ)
        
        #rotate_x(cube[i], math.pi/4)
    cube_2d = []
    for i in range(len(cube)):
        cube_2d.append((project_point(cube[i])))
        cube_2d[i] = (cube_2d[i][0] + WIDTH / 2, cube_2d[i][1] + HEIGHT / 2)
        
    for e in edges:
        pg.draw.line(screen, (255,255,255), cube_2d[e[0]-1], cube_2d[e[1]-1])

def draw_x():
    pg.draw.line(screen, (255, 0, 0), (0, HEIGHT / 2), (WIDTH, HEIGHT / 2))

def draw_y():
    pg.draw.line(screen, (0, 255, 0), (WIDTH / 2, 0), (WIDTH / 2, HEIGHT))

rotX = 0
rotY = 0
rotZ = 0
run = True
while run:
    for e in pg.event.get():
        if e.type == pg.QUIT:
            run = False
    
    keys = pg.key.get_pressed()
    if keys[pg.K_a]:
        rotY -= 0.1
    if keys[pg.K_d]:
        rotY += 0.1
    if keys[pg.K_w]:
        rotX += 0.1
    if keys[pg.K_s]:
        rotX -= 0.1
    if keys[pg.K_q]:
        rotZ += 0.1
    if keys[pg.K_e]:
        rotZ -= 0.1
        

    screen.fill(0)
    
    draw_x()
    draw_y()
    draw_cube(-100,-100, -100, 200, rotX, rotY, rotZ)
    
    
    clock.tick(60)
    pg.display.flip()
 
pg.quit()