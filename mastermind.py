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
        self.attempts_nb = 1  # We are at the firsr attempt when the game starts

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
        self.COLOR_TO_GUESS = random.sample(self.COLOR_NUM, 4) # Randomly generates 4 colors to guess
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
        validate_box = validate_text.get_rect(center=(SCREEN_WIDTH/6 + 400 + 75, (SCREEN_HEIGHT/10 + 65*self.attempts_nb + 35)+self.SPACING*(self.attempts_nb-1)))
        self.screen.blit(validate_text, validate_box)
        pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect((SCREEN_WIDTH/6 + 100*4, (SCREEN_HEIGHT/10 +65*self.attempts_nb)+self.SPACING*(self.attempts_nb-1)), (150, 70)), width=5)

    
    def handle_choice(self):
        self.validate_choice = True
        print('handling choice')
        if self.guess != self.COLOR_TO_GUESS and 0 not in self.guess and self.attempts_nb <= 5:
            well_placed = len([i for i, j in zip(self.guess, self.COLOR_TO_GUESS) if i == j])
            misplaced = len([i for i in self.guess if i in self.COLOR_TO_GUESS]) - well_placed # Get the number of valid colors in the guess that are not in the correct position
            
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
                    if event.key == K_a or K_q or event.key == K_ESCAPE:
                        return 'quit'
                if event.type == pygame.MOUSEBUTTONDOWN:
                    return 'click'


    def handle_click(self, mouse_pos):
        # print('mouse_pos', mouse_pos)
        for i in range(8):
            # if the player clicks on a color
            if SCREEN_WIDTH/8*i < mouse_pos[0] < SCREEN_WIDTH/8*(i+1) and 0 < mouse_pos[1] < SCREEN_HEIGHT/10:
                self.picked_color = self.COLOR_NUM[i]

                self.screen.fill((0, 0, 0), pygame.Rect((SCREEN_WIDTH*5/6/2 - 125, SCREEN_HEIGHT/10 + self.SPACING*2/3), (250, 30)))          # erase previous color picked prompt
                color_picked_prompt = self.font.render('Color picked: %s' % self.picked_color.replace('_', ' '), True, (255, 255, 255))
                color_picked_box = color_picked_prompt.get_rect(center=(SCREEN_WIDTH*5/6/2, SCREEN_HEIGHT/10 + self.SPACING))           # get the box to display the text
                self.screen.blit(color_picked_prompt, color_picked_box) 
                print('picked_color', self.picked_color)
        for i in range(4):
            # if the plater clicks on a circle and he has a picked color
            if self.circles_center[i][0] - 35 < mouse_pos[0] < self.circles_center[i][0] + 35 and self.circles_center[i][1] - 35 < mouse_pos[1] < self.circles_center[i][1] + 35 \
                and self.picked_color is not None:
                self.guess[i] = self.picked_color
                pygame.draw.circle(self.screen, COLOR_DICT[self.picked_color], self.circles_center[i], 30)
                self.picked_color = None
                self.screen.fill((0, 0, 0), pygame.Rect((SCREEN_WIDTH*5/6/2 - 250/2, SCREEN_HEIGHT/10 + self.SPACING*2/3), (250, 30)))   # erase previous color picked prompt
                print('guess', self.guess)
        # if the player clicks on the validate button
        if SCREEN_WIDTH/6 + 400< mouse_pos[0] < SCREEN_WIDTH/6 + 400 + 150 and (SCREEN_HEIGHT/10 +65*self.attempts_nb)+self.SPACING*(self.attempts_nb-1) < mouse_pos[1] <\
           (SCREEN_HEIGHT/10 +65*self.attempts_nb)+self.SPACING*(self.attempts_nb-1) + 70:
            self.handle_choice()
            if self.attempts_nb <= 5:    # Prevent the game from drawing another round when the game if finished
                    self.draw_round()
            self.screen.fill((0, 0, 0), pygame.Rect((SCREEN_WIDTH*5/6/2 - 250/2, SCREEN_HEIGHT/10 + self.SPACING*2/3), (250, 30)))      # erase previous color picked prompt
            print('validated guess', self.guess)

    def result(self):
        if self.guess == self.COLOR_TO_GUESS:
            return 'win'
        if self.guess != self.COLOR_TO_GUESS and self.attempts_nb > 5:
            return 'lose'
        if self.guess != self.COLOR_TO_GUESS and self.attempts_nb < 5:
            return 'continue'


    def game_over(self, result):
        game_over_text = self.font.render('You %s !' % result, True, (255, 255, 255))
        if self.attempts_nb <= 3:
            game_over_box = game_over_text.get_rect(center=(SCREEN_WIDTH*5/6/2, SCREEN_HEIGHT/2))
        else:
            game_over_box = game_over_text.get_rect(center=(SCREEN_WIDTH*5/6/2, SCREEN_HEIGHT/2 + self.SPACING*(self.attempts_nb-1)))
        
        play_again_text = self.font.render('Play again ?', True, (255, 255, 255))
        play_again_box = play_again_text.get_rect(center=(SCREEN_WIDTH*5/6/2, SCREEN_HEIGHT/2 + self.SPACING*(self.attempts_nb+1)))

        pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect((SCREEN_WIDTH*5/6/2 - 75, SCREEN_HEIGHT/2 + self.SPACING*(self.attempts_nb+.575)), (150, 30)), width=5)
        self.screen.blit(play_again_text, play_again_box)
        self.screen.blit(game_over_text, game_over_box)
        pygame.display.flip() # update the screen (needed to display the changes because of the get input after getting into a while True loop and preventing 
                              # the function self.play to update the screen itself)


    def get_input_after_game_over(self):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    return 'quit'
                if event.type == KEYDOWN:
                    if event.key == K_a or K_q or event.key == K_ESCAPE:
                        return 'quit'
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    # if the player clicks on the play again button
                    if SCREEN_WIDTH*5/6/2 - 75 < mouse_pos[0] < SCREEN_WIDTH*5/6/2 + 75 and SCREEN_HEIGHT/2 + self.SPACING*(self.attempts_nb+.575) < mouse_pos[1] <\
                    SCREEN_HEIGHT/2 + self.SPACING*(self.attempts_nb+.575) + 30:
                        print('played again')
                        self.attempts_nb = 1  # Reset the number of attempts since we restart the game
                        self.play_again()
                        return 'play_again'


    def play(self):
        self.generate_colors_to_guess()
        print(self.COLOR_TO_GUESS)
        self.create_ui()
        self.draw_round()
        game_over = False
        while not game_over:
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
                    self.game_over('win')
                    game_over = True
                if self.result() == 'lose':
                    print("You lose")
                    self.game_over('lose')
                    game_over = True
                self.validate_choice = False
                self.guess = [0] * 4 # resets the guess for next round
            if game_over:
                key = self.get_input_after_game_over()
                if key == 'quit':
                    break
                


    def play_again(self):
        print('you chose to play again')
        self.play()


if __name__ == '__main__':
    game = Mastermind()
    game.play()