import pygame
from pygame.locals import *
import random

# setting up colors
COLORS_DICT = {
    'red': (255, 0, 0),
    'orange': (255, 165, 0),
    'yellow': (255, 255, 0),
    'cyan': (0, 255, 255),
    'blue': (0, 0, 255),
    'green': (0, 255, 0),
    'purple': (128, 0, 128),
    'pink': (255, 192, 203),
}

# setting up window's width & height
SCREEN_WIDTH, SCREEN_HEIGHT = 900, 1000

class Mastermind:
    def __init__(self):
        """
        In this function, class's constants and globals parameters are defined.
        """
        self.WINDOW_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
        self.SPACING = 35
        self.COLORS_RGB = list(COLORS_DICT.keys())
        self.COLOR_TO_GUESS = [0] * 4

        self.guess = [0] * 4
        self.pickedColor = None
        self.confirmChoice = False
        self.attemptsNb = 1  # First attempt, when the game starts

        pygame.init()
        pygame.display.set_caption('Mastermind')
        icon = pygame.image.load('icon/png_icon.png')
        pygame.display.set_icon(icon)
        pygame.display.set_mode(self.WINDOW_SIZE)
        pygame.font.init()
        self.font = pygame.font.SysFont('Roboto', 30)
        self.checkPlacementFont = pygame.font.SysFont('Roboto', 20)
        self.screen = pygame.display.set_mode(self.WINDOW_SIZE)
        

    def generateColorsToGuess(self):
        """
        This function randomly choses 4 colors from const COLORS_DICT.
        """
        self.COLOR_TO_GUESS = random.sample(self.COLORS_RGB, 4) # Randomly generates 4 colors to guess
        return self.COLOR_TO_GUESS   


    def createUI(self):
        """
        This function creates the UI (User Interface) by placing colors and text areas.
        """
        self.screen.fill((0, 0, 0))
        
        # creating area for each color 
        for i in range(8):
            colorWidth = SCREEN_WIDTH/8
            colorHeight = SCREEN_HEIGHT/10
            if i % 2 != 0:
                # prevents a 1 pixel gap between some colors  when screen width/8 isn't an integer (always happens on odd iterations)
                colorWidth += 1 # probably not the best way to do it but it works

            pygame.draw.rect(self.screen, COLORS_DICT[self.COLORS_RGB[i]], pygame.Rect(
                (SCREEN_WIDTH/8*i, 0), (colorWidth, colorHeight)))

        # filling in black the remaining unused space
        pygame.draw.line(self.screen, (255, 255, 255), (0, SCREEN_HEIGHT/10), (SCREEN_WIDTH, SCREEN_HEIGHT/10), 5)
        pygame.draw.line(self.screen, (255, 255, 255), (SCREEN_WIDTH*4/5, SCREEN_HEIGHT/10), (SCREEN_WIDTH*4/5, SCREEN_HEIGHT), 5)
        
        # setting up text & box areas
        placementText = self.checkPlacementFont.render('Well placed  -  Misplaced', True, (255, 255, 255))
        placementBox = placementText.get_rect(center=(
            SCREEN_WIDTH*17/20 + 45, SCREEN_HEIGHT/10 + 25))
        self.screen.blit(placementText, placementBox)


    def drawRound(self):
        """
        This function create areas in which user puts his colors guessed.
        """
        # setting up user inputs 
        self.circlesCenter = []
        for i in range(4):
            pygame.draw.circle(self.screen, (255, 255, 255), (SCREEN_WIDTH/6 + 100*i, SCREEN_HEIGHT/10 +100*self.attemptsNb), 35, width=5)
            self.circlesCenter.append((SCREEN_WIDTH/6 + 100*i, SCREEN_HEIGHT/10 +100*self.attemptsNb))

        # Create the text 'Confirm' and then create a box to place it 
        confirmText = self.font.render('Confirm', True, (255, 255, 255))
        confirmBox = confirmText.get_rect(center=(
            SCREEN_WIDTH/6 + 400 + 75, (SCREEN_HEIGHT/10 + 65*self.attemptsNb + 35)+self.SPACING*(self.attemptsNb-1)))
        self.screen.blit(confirmText, confirmBox)
        # Draw the rectangle around the 'Confirm' text
        pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(
            (SCREEN_WIDTH/6 + 100*4, (SCREEN_HEIGHT/10 +65*self.attemptsNb)+self.SPACING*(self.attemptsNb-1)), (150, 70)), width=5)

    
    def handleChoice(self):
        """
        This function checks the user's choices, if the choiced colors are good (each one), if the user still have some choices and finally 
        if the colors combine is the winner one.
        """
        self.confirmChoice = True
        print('handling choice')
        if self.guess != self.COLOR_TO_GUESS and 0 not in self.guess and self.attemptsNb <= 5:
            wellPlaced = len([i for i, j in zip(self.guess, self.COLOR_TO_GUESS) if i == j])
            misplaced = len([i for i in self.guess if i in self.COLOR_TO_GUESS]) - wellPlaced # Get the number of valid colors in the guess that are not in the correct position
            
            wellPlacedText = self.font.render(str(wellPlaced), True, (255, 255, 255))
            misplacedText = self.font.render(str(misplaced), True, (255, 255, 255))
            wellPlacedBox = wellPlacedText.get_rect(center=(
                SCREEN_WIDTH*17/20, (SCREEN_HEIGHT/10 + 65*self.attemptsNb + 35)+self.SPACING*(self.attemptsNb-1)))
            misplacedBox = misplacedText.get_rect(center=(
                SCREEN_WIDTH*19/20, (SCREEN_HEIGHT/10 + 65*self.attemptsNb + 35)+self.SPACING*(self.attemptsNb-1)))

            self.screen.blit(wellPlacedText, wellPlacedBox)
            self.screen.blit(misplacedText, misplacedBox)
            self.attemptsNb += 1
        

    def get_key(self):
        """
        This function track user keyboard's activity and close the Mastermind's window if needed.
        """
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    return 'quit'
                elif event.type == KEYDOWN:
                    if event.key == K_a or K_q or event.key == K_ESCAPE:
                        return 'quit'
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    return 'click'


    def handleClick(self, mouse_pos):
        """
        This function handle every click the user makes and acts in consequence. For example, if the player clicks on a color, on a circle,
        on the confirm button etc.
        """
        # print('mouse_pos', mouse_pos)
        
        for i in range(8):
            # if the player clicks on a color
            if SCREEN_WIDTH/8*i < mouse_pos[0] < SCREEN_WIDTH/8*(i+1) and 0 < mouse_pos[1] < SCREEN_HEIGHT/10:
                self.pickedColor = self.COLORS_RGB[i]
                self.screen.fill((0, 0, 0), pygame.Rect(
                    (SCREEN_WIDTH*5/6/2 - 125, SCREEN_HEIGHT/10 + self.SPACING*2/3), (250, 30))) # erase previous color picked prompt
                colorPickedPrompt = self.font.render('Color picked: %s' % self.pickedColor.replace('_', ' '), True, (255, 255, 255))
                colorPickedBox = colorPickedPrompt.get_rect(center=(
                    SCREEN_WIDTH*5/6/2, SCREEN_HEIGHT/10 + self.SPACING)) # get the box to display the text
                self.screen.blit(colorPickedPrompt, colorPickedBox)
                print('picked color :', self.pickedColor)
        
        for i in range(4):
            # if the player clicks on a circle and he has a picked color
            if self.circlesCenter[i][0] - 35 < mouse_pos[0] < self.circlesCenter[i][0] + 35 \
            and self.circlesCenter[i][1] - 35 < mouse_pos[1] < self.circlesCenter[i][1] + 35 and self.pickedColor is not None:
                self.guess[i] = self.pickedColor
                pygame.draw.circle(self.screen, COLORS_DICT[self.pickedColor], self.circlesCenter[i], 30)
                self.pickedColor = None
                self.screen.fill((0, 0, 0), pygame.Rect(
                    (SCREEN_WIDTH*5/6/2 - 250/2, SCREEN_HEIGHT/10 + self.SPACING*2/3), (250, 30))) # erase previous color picked prompt
                print('guess :', self.guess)

        # if the player clicks on the confirm button
        if SCREEN_WIDTH/6 + 400< mouse_pos[0] < SCREEN_WIDTH/6 + 400 + 150 \
        and (SCREEN_HEIGHT/10 +65*self.attemptsNb)+self.SPACING*(self.attemptsNb-1) < mouse_pos[1] \
        < (SCREEN_HEIGHT/10 +65*self.attemptsNb)+self.SPACING*(self.attemptsNb-1) + 70: # pretty huge condition not gonna lie
            self.handleChoice() 
            if self.attemptsNb <= 5:    # Prevent the game from drawing another round when the game if finished
                self.drawRound()
            self.screen.fill((0, 0, 0), pygame.Rect((SCREEN_WIDTH*5/6/2 - 250/2, SCREEN_HEIGHT/10 + self.SPACING*2/3), (250, 30))) # erase previous color picked prompt
            print('confirmed guess', self.guess)

    def result(self):
        """
        This function returns the statement of the game : if the user won or lost.
        """
        if self.guess == self.COLOR_TO_GUESS:
            return 'won'
        elif self.guess != self.COLOR_TO_GUESS and self.attemptsNb > 5:
            return 'lost'
        elif self.guess != self.COLOR_TO_GUESS and self.attemptsNb < 5:
            return 'continue'


    def gameOver(self, result):
        """
        This function is called once the game is done. This function shows the result and ask the user if he wants to play again.
        The function admit 1 arg :
        result (type : str) => which is actually the value returned by the function result().
        """
        gameOverText = self.font.render('You %s !' % result, True, (255, 255, 255))
        if self.attemptsNb <= 3:
            gameOverBox = gameOverText.get_rect(center=(
                SCREEN_WIDTH*5/6/2, SCREEN_HEIGHT/2))
        else:
            gameOverBox = gameOverText.get_rect(center=(
                SCREEN_WIDTH*5/6/2, SCREEN_HEIGHT/2 + self.SPACING*(self.attemptsNb-1)))
        
        playAgainText = self.font.render('Play again ?', True, (255, 255, 255))
        playAgainBox = playAgainText.get_rect(center=(
            SCREEN_WIDTH*5/6/2, SCREEN_HEIGHT/2 + self.SPACING*(self.attemptsNb+1)))

        pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(
            (SCREEN_WIDTH*5/6/2 - 75, SCREEN_HEIGHT/2 + self.SPACING*(self.attemptsNb+.575)), (150, 30)), width=5)
        self.screen.blit(playAgainText, playAgainBox)
        self.screen.blit(gameOverText, gameOverBox)
        pygame.display.flip() # update the screen (needed to display the changes because of the get input after getting into a while True loop and preventing 
                              # the function self.play to update the screen itself)


    def get_GameOverInput(self):
        """
        This function act depending on the user decision, if he wants to play again (by starting a new game) or not (by closing the window).
        """
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    return 'quit'
                elif event.type == KEYDOWN:
                    if event.key == K_a or K_q or event.key == K_ESCAPE:
                        return 'quit'
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    # if the player clicks on the play again button
                    if SCREEN_WIDTH*5/6/2 - 75 < mouse_pos[0] < SCREEN_WIDTH*5/6/2 + 75 and \
                         SCREEN_HEIGHT/2 + self.SPACING*(self.attemptsNb+.575) < mouse_pos[1] < SCREEN_HEIGHT/2 + self.SPACING*(self.attemptsNb+.575) + 30:
                        print('played again')
                        self.attemptsNb = 1  # Reset the number of attempts since we restart the game
                        self.playAgain()
                        return 'play again'


    def play(self):
        """
        Main function, makes the game works.
        """
        self.generateColorsToGuess()
        print(self.COLOR_TO_GUESS)
        self.createUI()
        self.drawRound()
        gameOver = False
        while not gameOver:
            pygame.display.flip()
            key = self.get_key()
            if key == 'quit':
                break
            elif key == 'choose':
                self.handleChoice()
                self.drawRound()
            elif key == 'click':
                self.handleClick(pygame.mouse.get_pos())
            if self.confirmChoice == True:
                print('confirmed')
                if self.result() == 'won':
                    print('You won!')
                    self.gameOver('won')
                    gameOver = True
                elif self.result() == 'lost':
                    print("You lost")
                    self.gameOver('lost')
                    gameOver = True
                self.confirmChoice = False
                self.guess = [0] * 4 # resets the guess for next round
            if gameOver:
                key = self.get_GameOverInput()
                if key == 'quit':
                    break
                


    def playAgain(self):
        """
        This function starts a new game.
        """
        print('you chose to play again')
        self.play()


if __name__ == '__main__':
    game = Mastermind()
    game.play()