"""
An interactive file, built on pygame, to display a racetrack.
Basic shell from MarquisLP Github.

Revision history:
@Antonio & @Colin (2/16/19) created file
@Colin (2/16/19 5:38pm) added a basic shell for a pygame loop
"""
import sys
import pygame
from pygame.locals import *
# Import additional modules here.


# Feel free to edit these constants to suit your requirements.
FRAME_RATE = 60.0
SCREEN_SIZE = (640, 480)
degree = 0
blue = (0,0,255)

class car:
    def __init__(self, rotation, location, points, width, height):
        self.rotation = 0
        self.location = 0
        self.points = (80, 0, 40, 30)
        self.width = 10
        self.height = 10

    def draw_rect(self):
        pygame.draw.rect(game_screen,blue,(200,150,100,50))


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

        # #create new surface with white BG
        # surf =  pygame.Surface((100, 100))
        # surf.fill((255, 255, 255))
        # #set a color key for blitting
        # surf.set_colorkey((255, 0, 0))

        # #create shapes so you can tell rotation is happenning
        # bigger =  pygame.Rect(0, 0, 100, 50)
        # smaller = pygame.Rect(25, 50, 50, 50)

        # #draw those two shapes to that surface
        # pygame.draw.rect(surf, (100, 0, 0), bigger)
        # pygame.draw.rect(surf, (100, 0, 0), smaller)

        # ##ORIGINAL UNCHANGED
        # #what coordinates will the static image be placed:
        # where = 200, 200

        # #draw surf to screen and catch the rect that blit returns
        # blittedRect = screen.blit(surf, where)

        # ##ROTATED
        # #get center of surf for later
        # oldCenter = blittedRect.center

        # #rotate surf by DEGREE amount degrees
        # rotatedSurf =  pygame.transform.rotate(surf, degree)

        # #get the rect of the rotated surf and set it's center to the oldCenter
        # rotRect = rotatedSurf.get_rect()
        # rotRect.center = oldCenter

        # #draw rotatedSurf with the corrected rect so it gets put in the proper spot
        # screen.blit(rotatedSurf, rotRect)

        #change the degree of rotation
        #degree += 5
        #if degree > 360:
        #    degree = 0

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