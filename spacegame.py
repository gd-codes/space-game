#_______________________________________________________________________________________________________________________
#
#                                                       Space Game
#-----------------------------------------------------------------------------------------------------------------------

import pygame
import random


# Initialize pygame
pygame.init()

# Game Window
res = scrwidth, scrheight = 1000, 700
screen = pygame.display.set_mode(res)
pygame.display.set_caption('Space game')

# Game clock
clock = pygame.time.Clock()
clock.tick(30)

# Load images
shipimg = pygame.image.load('spacecraft.png')
ast1 = pygame.image.load('asteroid1.png')
ast2 = pygame.image.load('asteroid2.png')
ast3 = pygame.image.load('asteroid3.png')
asteroids = [ast1, ast2, ast3]

# Game variables
gameover = False
score = 0

# Fonts
largetext = pygame.font.SysFont('consolas',115)
med_ocrfont = pygame.font.SysFont('ocr a extended', 40)
small_ocrfont = pygame.font.SysFont('ocr a extended', 15)
buttonfont = pygame.font.SysFont('fixedsys',20)


def message_display(text, font, x, y):
    """Displays a text message"""
    textsurface = font.render(text, True, (255,255,255))
    textrect = textsurface.get_rect()
    textrect.center = (x, y)
    screen.blit(textsurface, textrect)


def choose_obstacle():
    """Picks a random obstacle"""
    global asteroids    
    return random.sample(asteroids, 1)[0]

def choose_ypos():
    """ Picks a random y starting position for an obstacle"""
    return random.randrange(-50, scrheight-50)
    

class Spaceship :
    """To create spaceship objects with associated data values"""
    
    def __init__(self, obj, x, y):
        self.image = obj
        self.x = x
        self.y = y
        self.y_change = 0
        self.width = 175
        
    def animate(self):
        """Updates the ship position"""
        screen.blit(self.image, (self.x, self.y))


class Obstacle :
    """To create obstacle objects with associated data values"""
    
    def __init__(self, obj, x, y):
        self.currentobstacle = obj
        self.x = x
        self.y = y
        if obj == ast1 :
            self.speed = 1
            self.width, self.height = 180, 180
        elif obj == ast2 :
            self.speed = 3
            self.width, self.height = 200, 75
        elif obj == ast3 :
            self.speed = 2
            self.width, self.height = 120, 120
        # The speeds and sizes above are fixed for those asteroids

    def animate(self):
        """Updates spacecraft position"""
        screen.blit(self.currentobstacle, (self.x, self.y))
    

def gameloop():
    """ Main tasks that keep the game running"""
    global res, shipimg, gameover, screen, score

    screen.fill((0,0,0))

    # Create obstacle and spaceship objects
    ship = Spaceship(shipimg, 50, scrheight/2)
    ship.y = (scrheight - ship.width) / 2
    obs1 = Obstacle(choose_obstacle(), scrwidth+150, choose_ypos())

    # Main loop
    while not gameover :

        # Check for events
        for event in pygame.event.get():
            # If window is closed
            if event.type == pygame.QUIT :
                pygame.quit()
                quit()
            #Key presses
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    ship.y_change = -1
                elif event.key == pygame.K_DOWN:
                    ship.y_change = 1
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    ship.y_change = 0
                    
        # Update spacecraft position            
        ship.animate()
        ship.y += ship.y_change
        if (ship.y < 0 - ship.width/2) or (ship.y > scrwidth - 2*ship.width):
            restartgame('You drove outside the screen !')

        # Check for crash
        if obs1.x < (ship.x + ship.width) and obs1.x > (ship.x + ship.width - obs1.width) :
            if obs1.y < (ship.y + ship.width) and obs1.y > (ship.y - obs1.height) :
                restartgame('You were hit by an asteroid !')

        # Update obstacle position 
        if obs1.x < -150 :
            obs1 = Obstacle(choose_obstacle(), scrwidth+150, choose_ypos())
            screen.fill((0,0,0))
            score += 1
        else :
            obs1.x -= obs1.speed
            

        # Display changes
        obs1.animate()
        message_display('Score : {}'.format(score), small_ocrfont, 55, 20)
        pygame.display.update()

    # To allow the window to be closed even after the main gameloop has been exited
    while True :
        for event in pygame.event.get():
                # If window is closed
                if event.type == pygame.QUIT :
                    pygame.quit()
                    quit()

    


def restartgame(reason):
    """Finishes/Begins a game"""
    global gameover
    gameover = True
    screen.fill((0,0,0))
    message_display('Game Over', largetext, scrwidth/2, scrheight/2 - 25)
    message_display(reason, med_ocrfont, scrwidth/2, scrheight/2 + 25)

    

        
                

if __name__ == '__main__' :

    gameloop()
            
#_______________________________________________________________________________________________________________________




