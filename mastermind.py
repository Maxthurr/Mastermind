import pygame
from pygame.locals import *
import random

COLOR_DICT = {                       # Dictionary of colors, you can modify them as you wish
    'red': (255, 0, 0),
    'orange': (255, 165, 0),
    'yellow': (255, 255, 0),
    'light_blue': (0, 255, 255),
    'blue': (0, 0, 255),
    'green': (0, 255, 0),
    'purple': (128, 0, 128),
    'pink': (255, 192, 203),
}

SCREEN_WIDTH = 900 # screen width, modify this to change the width of the window
SCREEN_HEIGHT = 1000 # screen height, modify this to change the height of the window

class Mastermind:
    def __init__(self):
        self.WINDOW_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
        self.SPACING = 35
        self.COLOR_NUM = list(COLOR_DICT.keys())
        self.COLOR_TO_GUESS = [0] * 4

        self.guess = [0] * 4
        self.picked_color = None
        self.validate_choice = False
        self.attempts_nb = 1

        pygame.init()
        pygame.display.set_caption('Mastermind')
        icon = pygame.image.load('icon/png_icon.png')
        pygame.display.set_icon(icon)
        pygame.display.set_mode(self.WINDOW_SIZE)
        pygame.font.init()
        self.font = pygame.font.SysFont('Roboto', 30)
        self.check_placement_font = pygame.font.SysFont('Roboto', 20)

        self.screen = pygame.display.set_mode(self.WINDOW_SIZE)

    def __str__(self):
        # Might need to change this 
        return str(self.COLOR_TO_GUESS)
        

    def generate_colors_to_guess(self):
        self.COLOR_TO_GUESS = [random.choice(self.COLOR_NUM) for i in range(4)]
        return self.COLOR_TO_GUESS   


    def create_ui(self):
        self.screen.fill((0, 0, 0))

        for i in range(8):
            rectangle_width = SCREEN_WIDTH/8
            rectangle_height = SCREEN_HEIGHT/10
            if i%2!=0:
                rectangle_width = SCREEN_WIDTH/8 + 1 # prevents a 1 pixel gap between some rectangles when screen width/8 isn't an integer (always happens on odd iterations)
                                                     # probably not the best way to do it but it works

            pygame.draw.rect(self.screen, COLOR_DICT[self.COLOR_NUM[i]], pygame.Rect((SCREEN_WIDTH/8*i, 0), (rectangle_width, rectangle_height)))

        pygame.draw.line(self.screen, (255, 255, 255), (0, SCREEN_HEIGHT/10), (SCREEN_WIDTH, SCREEN_HEIGHT/10), 5)
        pygame.draw.line(self.screen, (255, 255, 255), (SCREEN_WIDTH*4/5, SCREEN_HEIGHT/10), (SCREEN_WIDTH*4/5, SCREEN_HEIGHT), 5)

        placement_text = self.check_placement_font.render('Well placed  -  Misplaced', True, (255, 255, 255))
        placement_box = placement_text.get_rect(center=(SCREEN_WIDTH*17/20 + 45, SCREEN_HEIGHT/10 + 25))

        self.screen.blit(placement_text, placement_box)


    def draw_round(self):
        self.circles_center = []
        for i in range(4):
            pygame.draw.circle(self.screen, (255, 255, 255), (SCREEN_WIDTH/6 + 100*i, SCREEN_HEIGHT/10 +100*self.attempts_nb), 35, width=5)
            self.circles_center.append((SCREEN_WIDTH/6 + 100*i, SCREEN_HEIGHT/10 +100*self.attempts_nb))

        validate_text = self.font.render('Validate', True, (255, 255, 255))
        validate_box = validate_text.get_rect(center=(SCREEN_WIDTH/6 + 100*4 + 75, (SCREEN_HEIGHT/10 + 65*self.attempts_nb + 35)+self.SPACING*(self.attempts_nb-1)))
        self.screen.blit(validate_text, validate_box)
        pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect((SCREEN_WIDTH/6 + 100*4, (SCREEN_HEIGHT/10 +65*self.attempts_nb)+self.SPACING*(self.attempts_nb-1)), (150, 70)), width=5)

    
    def handle_choice(self):
        self.validate_choice = True
        print('handling choice')
        if self.guess != self.COLOR_TO_GUESS and self.attempts_nb <= 5:
            well_placed = len([i for i, j in zip(self.guess, self.COLOR_TO_GUESS) if i == j])
            misplaced = len([i for i in self.guess if i in self.COLOR_TO_GUESS]) - well_placed
            
            well_placed_text = self.font.render(str(well_placed), True, (255, 255, 255))
            misplaced_text = self.font.render(str(misplaced), True, (255, 255, 255))
            well_placed_box = well_placed_text.get_rect(center=(SCREEN_WIDTH*17/20, (SCREEN_HEIGHT/10 + 65*self.attempts_nb + 35)+self.SPACING*(self.attempts_nb-1)))
            misplaced_box = misplaced_text.get_rect(center=(SCREEN_WIDTH*19/20, (SCREEN_HEIGHT/10 + 65*self.attempts_nb + 35)+self.SPACING*(self.attempts_nb-1)))

            self.screen.blit(well_placed_text, well_placed_box)
            self.screen.blit(misplaced_text, misplaced_box)
            self.attempts_nb += 1
        

    def get_key(self):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    return 'quit'
                if event.type == KEYDOWN:
                    if event.key == K_a or event.key == K_ESCAPE:
                        return 'quit'
                    if event.key == K_RETURN:
                        return 'choose'
                if event.type == pygame.MOUSEBUTTONDOWN:
                    return 'click'


    def handle_click(self, mouse_pos):
        # print('mouse_pos', mouse_pos)
        for i in range(8):
            if SCREEN_WIDTH/8*i < mouse_pos[0] < SCREEN_WIDTH/8*(i+1) and 0 < mouse_pos[1] < SCREEN_HEIGHT/10:
                self.picked_color = self.COLOR_NUM[i]
                print('picked_color', self.picked_color)
        
        for i in range(4):
            if self.circles_center[i][0] - 35 < mouse_pos[0] < self.circles_center[i][0] + 35 and self.circles_center[i][1] - 35 < mouse_pos[1] < self.circles_center[i][1] + 35 and self.picked_color is not None:
                self.guess[i] = self.picked_color
                pygame.draw.circle(self.screen, COLOR_DICT[self.picked_color], self.circles_center[i], 30)
                self.picked_color = None
                print('guess', self.guess)
                
        if SCREEN_WIDTH/6 + 4*100 - 75 < mouse_pos[0] < SCREEN_WIDTH/6 + 4*100 + 75 and SCREEN_HEIGHT/10 + 100*self.attempts_nb - 35 < mouse_pos[1] < SCREEN_HEIGHT/10 + 100*self.attempts_nb + 35 and 0 not in self.guess:
            self.handle_choice()
            self.draw_round()
            print('validated guess', self.guess)
            return 'validate'

    def result(self):
        if self.guess == self.COLOR_TO_GUESS:
            return 'win'
        if self.guess != self.COLOR_TO_GUESS and self.attempts_nb > 5:
            return 'lose'
        if self.guess != self.COLOR_TO_GUESS and self.attempts_nb < 5:
            return 'continue'


    def play(self):
        self.generate_colors_to_guess()
        print(self.COLOR_TO_GUESS)
        self.create_ui()
        self.draw_round()
        while True:
            pygame.display.flip()
            key = self.get_key()
            if key == 'quit':
                break
            if key == 'choose':
                self.handle_choice()
                self.draw_round()
            if key == 'click':
                self.handle_click(pygame.mouse.get_pos())
            if self.validate_choice == True:
                print('validated')
                if self.result() == 'win':
                    print('You win!')
                    break
                    self.win()          # TO BE DONE: WIN SCREEN AND ADD A BUTTON TO PLAY AGAIN
                if self.result() == 'lose':
                    print("You lose")
                    break
                    self.game_over()    # TO BE DONE: LOSE SCREEN, ADD A BUTTON TO PLAY AGAIN AND SHOW THE SOLUTION
                self.validate_choice = False
                self.guess = [0] * 4


def play_again():
    game = Mastermind()
    game.play()


if __name__ == '__main__':
    game = Mastermind()
    game.play()