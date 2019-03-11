import os
import pygame
from math import tan, radians, degrees, copysign
from pygame.math import Vector2
import IO

CAR_ACCELERATION = 4
CAR_STEERING = 30
CAR_BRAKING = 8
MAX_VELOCITY = 80


class Car2:
    def __init__(self, x, y, angle=0.0, length=4, max_steering=30, max_acceleration=5.0):
        self.position = Vector2(x, y)
        self.velocity = Vector2(0.0, 0.0)
        self.angle = angle
        self.length = length
        self.max_acceleration = max(max_acceleration, CAR_BRAKING)
        self.max_steering = max_steering
        self.max_velocity = MAX_VELOCITY
        self.brake_deceleration = CAR_BRAKING
        self.free_deceleration = 2

        self.acceleration = 0.0
        self.steering = 0.0

    def update(self, dt):
        if self.velocity:
            print("vel: {} acc: {}".format(self.velocity, self.acceleration))
        self.velocity += (self.acceleration * dt, 0)
        self.velocity.x = max(-self.max_velocity, min(self.velocity.x, self.max_velocity))

        if self.steering:
            turning_radius = self.length / tan(radians(self.steering))
            angular_velocity = self.velocity.x / turning_radius
        else:
            angular_velocity = 0

        self.position += self.velocity.rotate(-self.angle) * dt
        self.angle += degrees(angular_velocity) * dt

    def move(self, movement, dt):
        if self.velocity.x < 0 and self.acceleration == -self.brake_deceleration:
            self.acceleration = 0
        elif self.velocity.x > 0 and self.acceleration == self.brake_deceleration:
            self.acceleration = 0
        if movement.front:
            if self.velocity.x < 0:
                self.acceleration = self.brake_deceleration
            else:
                self.acceleration += CAR_ACCELERATION * dt
        elif movement.back:
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

        if movement.right:
            self.steering -= CAR_STEERING * dt
        elif movement.left:
            self.steering += CAR_STEERING * dt
        else:
            self.steering = 0
        self.steering = max(-self.max_steering, min(self.steering, self.max_steering))

        # Logic
        self.update(dt)


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Car tutorial")
        width = 1280
        height = 720
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.ticks = 60
        self.exit = False

    def run(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(current_dir, "car.png")
        car_image = pygame.image.load(image_path)
        car = Car2(0, 0)
        ppu = 32

        while not self.exit:
            dt = self.clock.get_time() / 1000

            # Event queue
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit = True

            # User input
            pressed = pygame.key.get_pressed()
            pressed = list(map(bool, pressed))
            if(pressed[pygame.K_UP]):
                print("UP")
            if(pressed[pygame.K_DOWN]):
                print("DOWN")
            m = IO.Movement(pressed[pygame.K_LEFT], pressed[pygame.K_RIGHT], pressed[pygame.K_UP], pressed[pygame.K_DOWN])
            print(m)

            car.move(m, dt)

            # Drawing
            self.screen.fill((0, 0, 0))
            rotated = pygame.transform.rotate(car_image, car.angle)
            rect = rotated.get_rect()
            self.screen.blit(rotated, car.position * ppu - (rect.width / 2, rect.height / 2))
            pygame.display.flip()

            self.clock.tick(self.ticks)
        pygame.quit()


if __name__ == '__main__':
    game = Game()
    game.run()
