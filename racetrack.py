"""
An interactive file, built on pygame, to display a racetrack.
Basic shell from MarquisLP Github.

Revision history:
@Antonio & @Colin (2/16/19) created file
@Colin (2/16/19 5:38pm) added a basic shell for a pygame loop
@Colin (3/5/19 5:38pm) added basic movement (not finished but getting there)
@Colin (3/5/19 11:40pm) Finished basic movement combined aspects of maps antonio has made into the program. TODO: Make the rectangle visually rotate
@Parth (3/8/19 11:40am) Put most of the file into a if __name__ == '__main__' block
"""
import os
import pygame
import sys
import utils
import Car
import IO
import AI
import Map
import numpy as np
from pygame.locals import *
from math import tan, radians, degrees, copysign
from pygame.math import Vector2
import math

FRAME_RATE = 60.0
SCREEN_SIZE = (800, 600)
degree = 0
blue = (0,0,255)
IS_HUMAN = False
RESET = True

def pygame_modules_have_loaded():
    success = True

    if not pygame.display.get_init:
        success = False
    if not pygame.font.get_init():
        success = False
    if not pygame.mixer.get_init():
        success = False

    return success
       
if __name__ == '__main__':
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

        def get_human_move():
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
            return  IO.Movement(np_array)


        def hit(car, map):
            if RESET:
                car.angle = 90
                car.position = pygame.Vector2(*map.starting_point)
                car.velocity = pygame.Vector2(0, 0)
                car.steering = car.acceleration = 0
            else:      
                car.velocity = pygame.Vector2(-10, 0)

        def update(screen, dt, car, map, driver=None, h_car=None, FRAMES_STILL = 0):
            # Add in code to be run during each update cycle.
            # screen provides the PyGame Surface for the game window.
            # time provides the seconds elapsed since the last update.
           
            screen.fill((255,255,255))
            map.drawOnScreen(game_screen)


            if IS_HUMAN:
                movement = get_human_move()
            else:
                state = map.getState(car, screen)
                movement = driver.runAI(state)
                # print(movement)
                # print(state)

            rew = map.reward(car)
            car.move_car(movement, dt)
            car.draw(screen)
            driver.trainAI(state, movement, rew)

            # Punish the car for staying still for too long
            if car.velocity.x <= 10:
                FRAMES_STILL += 1

            if FRAMES_STILL == 180:
                rew = -50
                FRAMES_STILL = 0

            if h_car:
                mvmt = get_human_move()
                h_car.move_car(mvmt, dt)
                h_car.draw(screen)
                rew_h = map.reward(h_car)
                if rew_h == -100:
                    hit(h_car, map)
            
            if rew == 100:
                print("REWARD GATE REACHED!")
            elif rew == -100 or rew = -50:
                hit(car, map)


            #show the screen surface
            pygame.display.flip()
            pygame.display.update()

            return FRAMES_STILL

        # Add additional methods here.

        def main():
            prepare_test()

            map = Map.Map("donut")
            (x, y) = map.starting_point
            test_car = Car.Car(x,y, angle=90)
            human_car = Car.Car(x, y, angle=90)
            driver = AI.Driver()

            FRAMES_STILL = 0

            while True:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()

               

                milliseconds = clock.tick(FRAME_RATE)
                dt = milliseconds / 1000.0

                FRAMES_STILL = update(game_screen, dt, test_car, map, driver, human_car, FRAMES_STILL)

                sleep_time = (1000.0 / FRAME_RATE) - milliseconds
                if sleep_time > 0.0:
                    pygame.time.wait(int(sleep_time))
                else:
                    pygame.time.wait(1)

    main()