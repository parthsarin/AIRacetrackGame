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



class Car:
    """Initializes CAR class.
        :x the x position.
        :y the y postiion.
        :angle: Angle of the car’s body, relative to the world, in degrees
        :length: length of car chassis
        :width: width of car chassis
        :max_steering: maximum steering value in degrees
        :max_acceleration: value of acceleration, in meters per second squared
        :acceleration: current acceleration
        :steering:  current steering value, in degrees. Negative values mean that the wheels are turned to the right and positive – to the left.
        """
    def __init__(self, x, y, angle=90.0, length=40, width=60, max_steering=450, max_acceleration=10.0):
        self.position = Vector2(x, y)
        self.velocity = Vector2(0.0, 0.0)
        self.angle = angle
        self.length = length
        self.width = width
        self.max_acceleration = max_acceleration
        self.max_steering = max_steering
        self.max_velocity = 30
        self.brake_deceleration = 10
        self.free_deceleration = 2

        self.acceleration = 0.0
        self.steering = 0.0

    def update(self, dt):
        self.velocity += (self.acceleration * dt, 0)
        self.velocity.x = max(-self.max_velocity, min(self.velocity.x, self.max_velocity))

        if self.steering:
            turning_radius = self.length / tan(radians(self.steering))
            angular_velocity = self.velocity.x / turning_radius
        else:
            angular_velocity = 0

        #debug statement
        #print("Angular Velocity:", angular_velocity,"  steering:" ,self.steering)

        self.position += self.velocity.rotate(-self.angle) * dt
        self.angle += degrees(angular_velocity) * dt

    def draw(self):

        pygame.draw.rect(game_screen,blue,pygame.Rect((self.position[0],self.position[1]),(self.width, self.length)))





def pygame_modules_have_loaded():
    success = True

    if not pygame.display.get_init:
        success = False
    if not pygame.font.get_init():
        success = False
    if not pygame.mixer.get_init():
        success = False

    return success

def move_car (mvmt, car, dt) :
    
        if mvmt.front:# moving front
            if car.velocity.x < 0:
                car.acceleration = car.brake_deceleration
            else:
                car.acceleration += 1 * dt
        elif mvmt.back: # moving back
            if car.velocity.x > 0:
                car.acceleration = -car.brake_deceleration
            else:
                car.acceleration -= 1 * dt
        else:
            if abs(car.velocity.x) > dt * car.free_deceleration:
                car.acceleration = -copysign(car.free_deceleration, car.velocity.x)
            else:
                if dt != 0:
                    car.acceleration = -car.velocity.x / dt
        car.acceleration = max(-car.max_acceleration, min(car.acceleration, car.max_acceleration))
        #debug statement
        #print("mvmt.right", mvmt.right,"  mvmt.front:", mvmt.front)

        if mvmt.right or (mvmt.right and mvmt.front): # right
            car.steering -= 30 * dt
            print("test")
        elif mvmt.left or (mvmt.left and mvmt.front): #left
                car.steering += 30 * dt
        else:
            car.steering = 0 #Here is the problem it resets steering when you press forward and left/right
        car.steering = max(-car.max_steering, min(car.steering, car.max_steering))    
       

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
                

    def update(screen, dt, car, map):
        # Add in code to be run during each update cycle.
        # screen provides the PyGame Surface for the game window.
        # time provides the seconds elapsed since the last update.
       
        screen.fill((255,255,255))
        map.drawOnScreen(game_screen)
        car.update(dt)
        car.draw()

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

            # print("keys.right", keys.right,"  keys.front:", keys.front) debug statement

            move_car(movement, test_car, dt)

            update(game_screen, dt, test_car, map)

            sleep_time = (1000.0 / FRAME_RATE) - milliseconds
            if sleep_time > 0.0:
                pygame.time.wait(int(sleep_time))
            else:
                pygame.time.wait(1)

if __name__ == '__main__':
    main()