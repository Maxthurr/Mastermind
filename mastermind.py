import pygame
from pygame.locals import *
import random

COLOR_DICT = {
    'red': (255, 0, 0),
    'orange': (255, 165, 0),
    'yellow': (255, 255, 0),
    'light_blue': (0, 255, 255),
    'blue': (0, 0, 255),
    'green': (0, 255, 0),
    'purple': (128, 0, 128),
    'pink': (255, 192, 203),
}

SCREEN_WIDTH = 900 # screen width, modify this to change the size of the window
SCREEN_HEIGHT = 1000 # screen height, modify this to change the size of the window

class Mastermind:
    def __init__(self):
        self.WINDOW_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
        self.COLORS = COLOR_DICT
        self.COLOR_NUM = {i:list(self.COLORS.keys())[i] for i in range(len(self.COLORS))}
        self.COLOR_TO_GUESS = [0] * 4
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
        return str(self.COLOR_TO_GUESS)
        

    def generate_colors_to_guess(self):
        self.COLOR_TO_GUESS = [random.choice(list(self.COLOR_NUM.keys())) for i in range(4)]
        return self.COLOR_TO_GUESS   


    # NEED TO BE DONE: CREATE UI AND GET PLAYER'S CHOICE
    def handle_choice(self, choice):    # need to find a way to get player's choice
        self.guess = choice
        self.attempts_nb += 1
        return self.guess


    def create_ui(self):
        # TO BE DONE: CREATE UI
        self.screen.fill((0, 0, 0))

        for i in range(8):
            rectangle_width = SCREEN_WIDTH/8
            rectangle_height = SCREEN_HEIGHT/10
            if i%2!=0:
                rectangle_width = SCREEN_WIDTH/8 + 1 # prevents a 1 pixel gap between some rectangles when screen width/8 isn't an integer (always happens on odd iterations)
                                                     # probably not the best way to do it but it works

            pygame.draw.rect(self.screen, self.COLORS[self.COLOR_NUM[i]], pygame.Rect((SCREEN_WIDTH/8*i, 0), (rectangle_width, rectangle_height)))

        pygame.draw.line(self.screen, (255, 255, 255), (0, SCREEN_HEIGHT/10), (SCREEN_WIDTH, SCREEN_HEIGHT/10), 5)
        pygame.draw.line(self.screen, (255, 255, 255), (SCREEN_WIDTH*4/5, SCREEN_HEIGHT/10), (SCREEN_WIDTH*4/5, SCREEN_HEIGHT), 5)


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
        # Not sure if this is the best way to do it but still works
        if self.guess == self.COLOR_TO_GUESS:
            return 'win'
        if self.guess != self.COLOR_TO_GUESS and self.attempts_nb == 5:
            return 'lose'
        

    def play(self):
        self.generate_colors_to_guess()
        while True:
            self.create_ui()
            pygame.display.flip()
            key = self.get_key()
            if key == 'quit':
                break
            if key == 'choose':
                self.handle_choice()
            if self.result() == 'win':
                continue
                # TO BE DONE: WIN SCREEN AND ADD A BUTTON TO PLAY AGAIN
            if self.result() == 'lose':
                # TO BE DONE: LOSE SCREEN, ADD A BUTTON TO PLAY AGAIN AND SHOW THE SOLUTION
                continue


if __name__ == '__main__':
    game = Mastermind()
    game.play()