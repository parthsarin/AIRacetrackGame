"""
An interactive file, built on pygame, to display a racetrack.
Basic shell from MarquisLP Github.

Revision history:
@Antonio & @Colin (2/16/19) created file
@Colin (2/16/19 5:38pm) added a basic shell for a pygame loop
@Colin (3/5/19 5:38pm) added basic movement (not finished but getting there)
@Colin (3/5/19 11:40pm) Finished basic movement combined aspects of maps antonio has made into the program. TODO: Make the rectangle visually rotate
@Parth (3/6/19 12:10pm) Changed 'Movement' to 'Keys'. The reason is that the AI talks in the language of Movements, so I added another wrapper class so it will better interact with graphics
"""
import os
import pygame
import sys
import utils
import Car
import IO
import Map
import numpy as np
from pygame.locals import *
from math import tan, radians, degrees, copysign
from pygame.math import Vector2

FRAME_RATE = 60.0
SCREEN_SIZE = (800, 600)
degree = 0
blue = (0,0,255)


def pygame_modules_have_loaded():
    success = True

    if not pygame.display.get_init:
        success = False
    if not pygame.font.get_init():
        success = False
    if not pygame.mixer.get_init():
        success = False

    return success
       

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
pygame.font.init()

if pygame_modules_have_loaded():
    game_screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption('Race!')
    clock = pygame.time.Clock()

    def prepare_test():
        # Add in any code that needs to be run before the game loop starts.
        # can add the ability to customize aspects of car here if we want

        pass

    def handle_input():
        # Handles user input
        # packages user input into the movement class
        # Keys(False, True, False, True) # left, right, up, down

        pressed = pygame.key.get_pressed()

        np_array = np.zeros(4)

        if pressed[pygame.K_UP]:
            np_array[2] = 1
                
        if pressed[pygame.K_DOWN]:
            np_array[3] = 1
       
        if pressed[pygame.K_RIGHT]:
            
            np_array[1] = 1
            
        if pressed[pygame.K_LEFT]:
            np_array[0] = 1
        #if pressed[pygame.K_UP] and pressed[pygame.K_RIGHT]: # for testing turning
        #    print("Both!Both!")

        return  IO.Movement(np_array)
                

    def update(screen, dt, movement, car, map):
        # Add in code to be run during each update cycle.
        # screen provides the PyGame Surface for the game window.
        # time provides the seconds elapsed since the last update.
       
        screen.fill((255,255,255))
        map.drawOnScreen(game_screen)
        car.move(movement, dt)
        car.draw(screen)

        #show the screen surface
        pygame.display.flip()
        pygame.display.update()

    # Add additional methods here.

    def main():
        prepare_test()

        map = Map.Map("square-list.map")
        (x, y) = map.starting_point
        test_car = Car(x,y)
        
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

           

            milliseconds = clock.tick(FRAME_RATE)
            dt = milliseconds / 1000.0

            movement = handle_input()
            update(game_screen, dt, movement, test_car, map)

            sleep_time = (1000.0 / FRAME_RATE) - milliseconds
            if sleep_time > 0.0:
                pygame.time.wait(int(sleep_time))
            else:
                pygame.time.wait(1)

if __name__ == '__main__':
    main()