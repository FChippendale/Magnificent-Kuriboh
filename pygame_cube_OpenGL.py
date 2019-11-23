import pygame
import sys
import winsound

#frequency = 440  # Set Frequency To 2500 Hertz
#duration = 100  # Set Duration To 1000 ms == 1 second
#winsound.Beep(frequency, duration)

from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

verticies = (
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, -1, 1),
    (-1, 1, 1),
)

edges = (
    (0, 1),
    (0, 3),
    (0, 4),
    (2, 1),
    (2, 3),
    (2, 7),
    (6, 3),
    (6, 4),
    (6, 7),
    (5, 1),
    (5, 4),
    (5, 7),
)

surfaces = (
    (4, 5, 1, 0),
    (1, 5, 7, 2),
    (4, 0, 3, 6),
    (0, 1, 2, 3),
    (3, 2, 7, 6),
    (6, 7, 5, 4),
)

gl_colors = (
    (0, 0, 1),
    (0, 1, 0),
    (1, 0, 0)
)

def Cube():
    glBegin(GL_QUADS)
    for i, surface in enumerate(surfaces):
        glColor3fv(gl_colors[i % 3])
        for vertex in surface:
            glVertex3fv(verticies[vertex])
    glEnd()
    
pygame.init()
display = (800, 600)
screen = pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

glEnable(GL_DEPTH_TEST)

glMatrixMode(GL_PROJECTION)
gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)

glMatrixMode(GL_MODELVIEW)
gluLookAt(0, -8, 0, 0, 0, 0, 0, 0, 1) #(first 3 are starting pos, second three are reference point, third three are direction of 'up')
viewMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)
glLoadIdentity()

pygame.event.get()
pygame.mouse.get_rel()
pygame.mouse.set_visible(0)
pygame.event.set_grab(1)

mouseMove = (0, 0)
prev_mouseMove = (0, 0)
up_down_mouseMove = 0

cur_pos = [0, -8] #X Z

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: pygame.quit(); sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE: pygame.quit(), sys.exit()
        if event.type == pygame.MOUSEMOTION:
            mouseMove = event.rel
            
            
               
    if mouseMove[0] == prev_mouseMove[0]:
        mouseMove = (0, mouseMove[1])
    if mouseMove[1] == prev_mouseMove[1]:
        mouseMove = (mouseMove[0], 0)    
    up_down_mouseMove += mouseMove[1]
        
    prev_mouseMove = mouseMove
    
    keypress = pygame.key.get_pressed() 
    glLoadIdentity() 
    
    glRotatef(up_down_mouseMove*0.1, 1.0, 0.0, 0.0)

    # init the view matrix
    glPushMatrix()
    glLoadIdentity()

    # apply the movment 
    if keypress[pygame.K_w]:
        cur_pos[1] += 0.1
        glTranslatef(0,0,0.1)
    if keypress[pygame.K_s]:
        cur_pos[1] -= 0.1
        glTranslatef(0,0,-0.1)
    if keypress[pygame.K_d]:
        cur_pos[0] += 0.1
        glTranslatef(-0.1,0,0)
    if keypress[pygame.K_a]:
        cur_pos[0] -= 0.1
        glTranslatef(0.1,0,0)
    
    glRotatef(mouseMove[0]*0.1, 0.0, 1.0, 0.0)

    glMultMatrixf(viewMatrix)
    viewMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)

    glPopMatrix()
    glMultMatrixf(viewMatrix)

    
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

    glPushMatrix()
    
    Cube()
    
    glPopMatrix()

    pygame.display.flip()
    pygame.time.wait(10)
    
