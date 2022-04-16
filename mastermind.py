import pygame
from pygame.locals import *
import numpy as np
import random

COLOR_DICT = {
    'yellow': (255, 255, 0),
    'red': (255, 0, 0),
    'green': (0, 255, 0),
    'blue': (0, 0, 255),
    'white': (255, 255, 255),
    'orange': (255, 165, 0),
    'pink': (255, 192, 203),
    'purple': (128, 0, 128),
}

SCREEN_WIDTH = 800 # screen width, modify this to change the size of the window
SCREEN_HEIGHT = 1000 # screen height, modify this to change the size of the window

class Mastermind:
    def __init__(self):
        self.WINDOW_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
        self.COLORS = COLOR_DICT
        self.COLOR_NUM = {i:list(self.COLORS.keys())[i] for i in range(len(self.COLORS))}
        self.COLOR_CHOICE = [0] * 4
        self.attempts_nb = 0

        pygame.init()
        pygame.display.set_caption('Mastermind')
        icon = pygame.image.load('icon/png_icon.png')
        pygame.display.set_icon(icon)
        pygame.display.set_mode(self.WINDOW_SIZE)
        pygame.font.init()
        self.font = pygame.font.SysFont('Roboto', 30)

        self.screen = pygame.display.set_mode(self.WINDOW_SIZE)

    def __str__(self):
        # Might need to change this 
        return str(self.COLOR_CHOICE)
        

    def generate_color_choice(self):
        self.COLOR_CHOICE = [random.choice(list(self.COLORS.keys())) for i in range(4)]
        return self.COLOR_CHOICE


    # NEED TO CREATE FUNCTION TO HANDLE CHOICE OF COLORS
    #def handle_choice(self, choice):       choice = list of color numbers -----> returns self.guess (list of color numbers)


    @staticmethod
    def get_key():
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    return 'quit'
                if event.type == KEYDOWN:
                    if event.key == K_a or event.key == K_ESCAPE:
                        return 'quit'
                    if event.key == K_RETURN:
                        return 'choose'


    def result(self):
        # TO BE DONE: CHECK IF THE GUESS IS CORRECT
        if self.guess == self.COLOR_CHOICE:
            return 'win'
        if self.guess != self.COLOR_CHOICE and self.attempts_nb == 5:
            return 'lose'
        

    def play(self):
        self.generate_color_choice()
        while True:
            #self.create_ui()
            pygame.display.flip()
            key = self.get_key()
            if key == 'quit':
                break
            if key == 'choose':
                self.handle_choice()
            if self.result() == 'win':
                continue
                # TO BE DONE: WIN SCREEN
            if self.result() == 'lose':
                # TO BE DONE: LOSE SCREEN
                continue


if __name__ == '__main__':
    game = Mastermind()
    game.play()