import pygame
import sys
import os
import numpy as np

def write_level(drawn_map, w, h):
    level_layout.write(str(h) + ' ' + str(w) + '\n')
    for i in range(h):
        layer = ''
        for ii in range(w):
            layer += str(int(drawn_map[ii][i])) + ' '
        layer += '\n'
        level_layout.write(layer)
    
    
colours = ((0, 0, 0), (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255))

level_layout = open('level_layout.txt', 'w+')
pygame.init()

w = 10
h = 10

SCREENWIDTH = 400
SCREENHEIGHT = (400 * h//w) 
SCREENSIZE = [SCREENWIDTH, SCREENHEIGHT]
screen = pygame.display.set_mode(SCREENSIZE)

#caption for the game
pygame.display.set_caption("Level editor")

points = np.zeros((w, h))

while True:
    pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE: write_level(points, w, h), pygame.quit(), level_layout.close(), sys.exit()
        #Here for any commands inside the for loop  
        if event.type == pygame.MOUSEBUTTONDOWN:
            points[int(pos[0] / SCREENWIDTH * w)][int(pos[1] / SCREENHEIGHT * h)] = (points[int(pos[0] / SCREENWIDTH * w)][int(pos[1] / SCREENHEIGHT * h)] + 1) % len(colours)

    for i in range(w):
        for ii in range(h):
            pygame.draw.polygon(screen, colours[int(points[i][ii])], ((i * SCREENWIDTH // w, (ii + 1) * SCREENHEIGHT // h), (i * SCREENWIDTH // w, ii * SCREENHEIGHT // h), ((i + 1) * SCREENWIDTH // w, ii * SCREENHEIGHT // h), ((i + 1) * 400 // w, (ii + 1) * 400 // h)))
            
    pygame.display.update()
