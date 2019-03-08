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

MAX_VELOCITY = 80


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
        self.max_velocity = MAX_VELOCITY
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

    def draw(self, screen):

        #pygame.draw.rect(game_screen,blue,pygame.Rect((self.position[0],self.position[1]),(self.width, self.length)))
        ppu = 32
        car_image = pygame.image.load(image_path)
        rotated = pygame.transform.rotate(car_image, self.angle)
        rect = rotated.get_rect()
        screen.blit(rotated, self.position * ppu - (rect.width / 2, rect.height / 2))



    def move_car (self, mvmt, dt) :
        
        if mvmt.front:# moving front
            if self.velocity.x < 0:
                self.acceleration = self.brake_deceleration
            else:
                self.acceleration += 1 * dt
        elif mvmt.back: # moving back
            if self.velocity.x > 0:
                self.acceleration = -self.brake_deceleration
            else:
                self.acceleration -= 1 * dt
        else:
            if abs(self.velocity.x) > dt * self.free_deceleration:
                self.acceleration = -copysign(self.free_deceleration, self.velocity.x)
            else:
                if dt != 0:
                    self.acceleration = -self.velocity.x / dt
        self.acceleration = max(-self.max_acceleration, min(self.acceleration, self.max_acceleration))
    #debug statement
    #print("mvmt.right", mvmt.right,"  mvmt.front:", mvmt.front)

        if mvmt.right or (mvmt.right and mvmt.front): # right
            self.steering -= 30 * dt
            
        elif mvmt.left or (mvmt.left and mvmt.front): #left
                self.steering += 30 * dt
        else:
            self.steering = 0 #Here is the problem it resets steering when you press forward and left/right
        self.steering = max(-self.max_steering, min(self.steering, self.max_steering))