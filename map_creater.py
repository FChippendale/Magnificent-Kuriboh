import pygame
import sys
import os

level_layout = open('level_layout.txt', 'w+')
pygame.init()

#Right way
SCREENWIDTH = 400
SCREENHEIGHT = 400
SCREENSIZE = [SCREENWIDTH, SCREENHEIGHT]
screen = pygame.display.set_mode(SCREENSIZE)

#caption for the game
pygame.display.set_caption("Level editor")

points = []

while True:
    pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE: pygame.quit(), level_layout.close(), sys.exit()
        #Here for any commands inside the for loop  
        if event.type == pygame.MOUSEBUTTONDOWN:
            points += [pos]
    
    if len(points) == 2:
        pygame.draw.line(screen, (255, 255, 255), points[0], points[1], 1)
        wall = str(points[0][0] // 10).zfill(3) + "," + str(points[0][1] // 10).zfill(3) + " " + str(points[1][0] // 10).zfill(3) + "," + str(points[1][1] // 10).zfill(3) + '\n'
        level_layout.write(wall)
        points = []

    #beware of the positioning of this line. It should be inside the while
    #for all the commands that need to be executed inside the while
    pygame.display.update()
    
