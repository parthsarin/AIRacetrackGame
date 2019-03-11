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

current_dir = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(current_dir, "car.png")

CAR_ACCELERATION = 40
CAR_STEERING = 3.5
CAR_BRAKING = 30
MAX_VELOCITY = 160
MAX_ACCELERATION = 40
CAR_PIXEL_HEIGHT = 60
CAR_PIXEL_WIDTH = 30



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
    def __init__(self, x, y, angle=0.0, max_steering=30):
        self.position = Vector2(x, y)
        self.velocity = Vector2(0.0, 0.0)
        self.angle = angle
        self.length = 4
        self.max_acceleration = MAX_ACCELERATION
        self.max_steering = max_steering
        self.max_velocity = MAX_VELOCITY
        self.brake_deceleration = CAR_BRAKING
        self.free_deceleration = 2
        self.p_length = CAR_PIXEL_HEIGHT
        self.p_width = CAR_PIXEL_WIDTH

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

    def draw(self, screen):

        #pygame.draw.rect(game_screen,blue,pygame.Rect((self.position[0],self.position[1]),(self.width, self.length)))
        ppu = 1
        car_image = pygame.image.load(image_path)
        car_image = pygame.transform.scale(car_image, (CAR_PIXEL_HEIGHT, CAR_PIXEL_WIDTH))
        rotated = pygame.transform.rotate(car_image, self.angle)
        rect = rotated.get_rect()
        #print("rect.width", rect.width, "  rect.height", rect.height, "  Final ", self.position * ppu - (rect.width / 2, rect.height / 2))
        screen.blit(rotated, self.position* ppu - (rect.width / 2, rect.height / 2))


    def move_car (self, mvmt, dt) :
        if self.velocity.x < 0 and self.acceleration == -self.brake_deceleration:
            self.acceleration = 0
        elif self.velocity.x > 0 and self.acceleration == self.brake_deceleration:
            self.acceleration = 0
        
        if mvmt.front:# moving front
            if self.velocity.x < 0:
                self.acceleration = self.brake_deceleration
            else:
                self.acceleration += CAR_ACCELERATION * dt
        elif mvmt.back: # moving back
            if self.velocity.x > 0:
                self.acceleration = -self.brake_deceleration
            else:
                self.acceleration -= CAR_ACCELERATION * dt
        else:
            if abs(self.velocity.x) > dt * self.free_deceleration:
                self.acceleration = -copysign(self.free_deceleration, self.velocity.x)
            else:
                if dt != 0:
                    self.acceleration = -self.velocity.x / dt
        self.acceleration = max(-self.max_acceleration, min(self.acceleration, self.max_acceleration))

        if mvmt.right:
            self.steering -= CAR_STEERING * dt
        elif mvmt.left:
                self.steering += CAR_STEERING * dt
        else:
            self.steering = 0
        self.steering = max(-self.max_steering, min(self.steering, self.max_steering))

        self.update(dt)