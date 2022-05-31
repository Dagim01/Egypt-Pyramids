import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

vertexes = (
    (-1, 1.5, 0.5),
    (-1.5, 0.5, -2),
    (0.5, 0.5, -2),
    (0.5, 2, -1),
    (-1.5, 2, -1)
)

edges = (
    (0,1),
    (0,2),
    (0,3),
    (1,2),
    (2,3),
    (4,0),
    (4,1),
    (4,3)
)

surfaces = (
    (0,1,2),
    (0,2,3),
    (0,4,3),
    (0,4,1),
    (4,1,2,3)
)

colors = (
    (0.5,0.35,0.05),
    (1.0, 0.5, 0.0),
    (0.1,0.0,0.0),
    (2,0.5,1.0),
    (1.0,1.0,0.0),
)


def cube(): 
    glBegin(GL_QUADS)
    for surface in surfaces:
        x = 0
        for vertex in surface:
            x += 1
            glColor3fv(colors[x])
            glVertex3fv(vertexes[vertex])

    glEnd()



    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertexes[vertex])
    glEnd()

def main():
    pygame.init()
    display = (1200,800)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
    glTranslate(0.0,0.0, -10)
    glRotate(15, 5, 10, 5)
    while True: 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit
                quit()
           

       
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        cube()
        pygame.display.flip()
        pygame.time.wait(10)
main() 