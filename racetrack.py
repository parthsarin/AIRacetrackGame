"""
An interactive file, built on pygame, to display a racetrack.
Basic shell from MarquisLP Github.

Revision history:
@Antonio & @Colin (2/16/19) created file
@Colin (2/16/19 5:38pm) added a basic shell for a pygame loop
@Colin (3/5/19 5:38pm) added basic movement (not finished but getting there)
"""
import os
import pygame
import sys
import pygame
import utils
import IO
import Map
import numpy as np
from pygame.locals import *
from math import tan, radians, degrees, copysign
from pygame.math import Vector2
# Import additional modules here.


# Feel free to edit these constants to suit your requirements.
FRAME_RATE = 60.0
SCREEN_SIZE = (640, 480)
degree = 0
blue = (0,0,255)

class car:
    """Initializes car calss.

        :x the x position.
        :y the y postiion.
        :angle: Angle of the car’s body, relative to the world, in degrees
        :length: length of car chassis
        :max_steering: maximum steering value in degrees
        :max_acceleration: value of acceleration, in meters per second squared
        :acceleration: current acceleration
        :steering:  current steering value, in degrees. Negative values mean that the wheels are turned to the right and positive – to the left.
        """
    def __init__(self, x, y, angle=0.0, length=4, max_steering=30, max_acceleration=5.0):
        self.position = Vector2(x, y)
        self.velocity = Vector2(0.0, 0.0)
        self.angle = angle
        self.length = length
        self.max_acceleration = max_acceleration
        self.max_steering = max_steering

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

        self.position += self.velocity.rotate(-self.angle) * dt
        self.angle += degrees(angular_velocity) * dt




def pygame_modules_have_loaded():
    success = True

    if not pygame.display.get_init:
        success = False
    if not pygame.font.get_init():
        success = False
    if not pygame.mixer.get_init():
        success = False

    return success
s
def move_car (mov_array, car) :

        if pressed[pygame.K_UP]: # moving up
                if car.velocity.x < 0:
                car.acceleration = car.brake_deceleration
                else:
                car.acceleration += 1 * dt
        elif pressed[pygame.K_DOWN]:
            if car.velocity.x > 0:
                    car.acceleration = -car.brake_deceleration
            else:
                car.acceleration -= 1 * dt
        elif pressed[pygame.K_SPACE]:
            if abs(car.velocity.x) > dt * car.brake_deceleration:
                car.acceleration = -copysign(car.brake_deceleration, car.velocity.x)
            else:
                car.acceleration = -car.velocity.x / dt
        else:
            if abs(car.velocity.x) > dt * car.free_deceleration:
                car.acceleration = -copysign(car.free_deceleration, car.velocity.x)
            else:
                if dt != 0:
                    car.acceleration = -car.velocity.x / dt
        car.acceleration = max(-car.max_acceleration, min(car.acceleration, car.max_acceleration))

        if pressed[pygame.K_RIGHT]:
            car.steering -= 30 * dt
        elif pressed[pygame.K_LEFT]:
                car.steering += 30 * dt
        else:
            car.steering = 0
        car.steering = max(-car.max_steering, min(car.steering, car.max_steering))    
       

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
pygame.font.init()

if pygame_modules_have_loaded():
    game_screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption('Test')
    clock = pygame.time.Clock()

    def declare_globals():
        # The class(es) that will be tested should be declared and initialized
        # here with the global keyword.
        # Yes, globals are evil, but for a confined test script they will make
        # everything much easier. This way, you can access the class(es) from
        # all three of the methods provided below.
        pass

    def prepare_test():
        # Add in any code that needs to be run before the game loop starts.
        pass

    def handle_input(key_name):
        # Add in code for input handling.
        # key_name provides the String name of the key that was pressed.
        pass

    def update(screen, time):
        # Add in code to be run during each update cycle.
        # screen provides the PyGame Surface for the game window.
        # time provides the seconds elapsed since the last update.
       
        screen.fill((40, 40, 40))

        testcar = car(0, 0, (200,150,100,50), 10, 10)
        testcar.draw_rect()
        #pygame.draw.rect(game_screen,blue,(200,150,100,50))

        #show the screen surface
        pygame.display.flip()
        pygame.display.update()

    # Add additional methods here.

    def main():
        declare_globals()
        prepare_test()

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == KEYDOWN:
                    key_name = pygame.key.name(event.key)
                    handle_input(key_name)

            milliseconds = clock.tick(FRAME_RATE)
            seconds = milliseconds / 1000.0
            update(game_screen, seconds)

            sleep_time = (1000.0 / FRAME_RATE) - milliseconds
            if sleep_time > 0.0:
                pygame.time.wait(int(sleep_time))
            else:
                pygame.time.wait(1)

if __name__ == '__main__':
    main()