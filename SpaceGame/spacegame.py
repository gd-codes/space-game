#_______________________________________________________________________________________________________________________
#
#                                                       Space Game
#-----------------------------------------------------------------------------------------------------------------------
# https://github.com/lemo-p/space-game.git
#-----------------------------------------------------------------------------------------------------------------------

import pygame
import random

def setup() :
    """Creates all global variables and objects required to start the game"""
    
    global res, screen, scrwidth, scrheight, clock, shipimg, asteroids, \
           gameover, score, high_score, ast1, ast2, ast3
    print('\n\nLoading ...')

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
    high_score = 0

def load_fonts():
    """Creates font objects"""
    global largetext, med_ocrfont, small_ocrfont, buttonfont
    
    largetext = pygame.font.SysFont('consolas',100)
    med_ocrfont = pygame.font.SysFont('lucida console', 40)
    small_ocrfont = pygame.font.SysFont('lucida console', 18)
    buttonfont = pygame.font.SysFont('fixedsys',30)

def start_screen():
    """ Initial screen that is displayed the first time the script is run"""
    global largetext, med_ocrfont, small_ocrfont
    
    res = scrwidth, scrheight = 1000, 700
    opening_window = pygame.display.set_mode(res)
    pygame.display.set_caption('Space game')

    inst1 = "Welcome to Space Game ! In this game, you will have to maneouvre a spacecraft "
    inst2 = "flying through an asteroid field and avoid being hit. The spacecraft moves in "
    inst3 = "a vertical line on the left-hand side of the screen, while asteroids come "
    inst4 = "flying at it from the right. You can use the up and down arrow keys to operate "
    inst5 = "the spacecraft. The game ends if you get hit by an asteroid or fly off the edge"
    inst6 = "of the screen, and your score will be the number of asteroids dodged. Enjoy playing !"
    instructions = [inst1, inst2, inst3, inst4, inst5, inst6]

    print("SPACE GAME\n")
    textsurface = largetext.render('Space Game', True, (255,255,255))
    textrect = textsurface.get_rect()
    textrect.center = (scrwidth/2, scrheight*0.2)
    opening_window.blit(textsurface, textrect)
    k = scrheight * 0.4
    for i in instructions :
        print(i, end = ' ')
        textsurface = small_ocrfont.render(i, True, (255,255,255))
        textrect = textsurface.get_rect()
        textrect.center = (scrwidth/2, k)
        opening_window.blit(textsurface, textrect)
        k += 20
    textsurface = med_ocrfont.render('Click anywhere to begin', True, (255,255,255))
    textrect = textsurface.get_rect()
    textrect.center = (scrwidth/2, scrheight*0.8)
    opening_window.blit(textsurface, textrect)

    pygame.display.update()

    started = False
    while not started :
        for event in pygame.event.get() :
            if event.type == pygame.MOUSEBUTTONDOWN :
                started = True
                pygame.display.quit()
    


def message_display(text, font, x, y, colour=(255,255,255)):
    """Displays a text message"""
    global screen
    textsurface = font.render(text, True, colour)
    textrect = textsurface.get_rect()
    textrect.center = (x, y)
    screen.blit(textsurface, textrect)


def choose_obstacle():
    """Picks a random obstacle"""
    global asteroids    
    return random.sample(asteroids, 1)[0]

def choose_ypos():
    """ Picks a random y starting position for an obstacle"""
    return random.randrange(0, scrheight-100)


class Button :
    """Creates a button on the screen"""

    def __init__(self, text, x, y, colour=(200,200,200), a_colour=(100,100,100)):
        global screen, buttonfont
        self.x = x
        self.y = y
        self.width = len(text)*20 + 30
        self.height = 50
        pygame.draw.rect(screen, colour, (x-self.width/2, y-self.height/2, self.width, self.height))
        message_display(text, buttonfont, x, y, (0,0,0))
        self.clicked = False


class Lasers :
    """To create laser objects with associated data values"""
    # Create Spaceship object before this
    def __init__(self, spship):
        self.ship = spship
        self.x2 = scrwidth - 50
        self.update_pos()
        self.active = False

    def update_pos(self):
        """Updates variables dependent on the spaseship's position"""
        self.x1 = self.ship.x + self.ship.width
        self.y1 = self.ship.y + (self.ship.width * 0.33)
        self.y2 = self.ship.y + (self.ship.width * 0.66)
        self.y3 = self.ship.y + (self.ship.width * 0.5)

    def fire(self):
        """Fires the lasers"""
        self.active = True
        self.update_pos()
        lbeam = pygame.draw.line(screen, (255,0,0), (self.x1,self.y1), (self.x2,self.y3), 5)
        rbeam = pygame.draw.line(screen, (255,0,0), (self.x1,self.y2), (self.x2,self.y3), 5)

    def deactivate(self):
        """Stops firing the lasers"""


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
        global screen
        screen.blit(self.image, (self.x, self.y))


class Obstacle :
    """To create obstacle objects with associated data values"""
    
    def __init__(self, obj, x, y):
        global ast1, ast2, ast3
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
        self.destroyed = False

    def animate(self):
        """Updates spacecraft position"""
        global screen
        if not self.destroyed :
            screen.blit(self.currentobstacle, (self.x, self.y))
    

def gameloop():
    """ Main tasks that keep the game running"""
    global res, shipimg, gameover, screen, score, small_ocrfont

    screen.fill((0,0,0))
    print('-----New Game started-----')

    # Create obstacle and spaceship objects
    ship = Spaceship(shipimg, 50, scrheight/2)
    ship.y = (scrheight - ship.width) / 2
    obs1 = Obstacle(choose_obstacle(), scrwidth+150, choose_ypos())
    lsr = Lasers(ship)

    for t in [3,2,1] :
        ship.animate()
        message_display(str(t), med_ocrfont, scrwidth/2, scrheight/2)
        pygame.display.update()
        pygame.time.delay(1000)
        screen.fill((0,0,0))

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
                elif event.key == pygame.K_SPACE :
                    lsr.fire()
                        
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    ship.y_change = 0
                    
        # Update spacecraft position            
        ship.animate()
        ship.y += ship.y_change
        if (ship.y < 0 - ship.width/2) or (ship.y > scrwidth - 2*ship.width):
            endgame('You drove outside the screen !')

        # Check for crash
        if obs1.x < (ship.x + ship.width) and obs1.x > (ship.x + ship.width - obs1.width) :
            if obs1.y < (ship.y + ship.width) and obs1.y > (ship.y - obs1.height) :
                if not obs1.destroyed :
                    endgame('You were hit by an asteroid !')

        # Check for successful laser blast
        if lsr.active :
            if obs1.x in range(int(lsr.x1), int(lsr.x2)) and obs1.y in range(int(lsr.y1 + 5), int(lsr.y2 - 5)) :
                obs1.destroyed = True

        # Update obstacle position 
        if obs1.x < -150 :
            obs1 = Obstacle(choose_obstacle(), scrwidth+150, choose_ypos())
            screen.fill((0,0,0))
            score += 1
        else :
            obs1.x -= obs1.speed
            

        # Display changes
        obs1.animate()
        message_display('Score : {}'.format(score), small_ocrfont, 60, 25)
        message_display('Highest : {}'.format(high_score), small_ocrfont, 70, 50)
        pygame.display.update()        
            
   


def endgame(reason):
    """Finishes a game"""
    
    global gameover, ng_btn, high_score, largetext, med_ocrfont
    gameover = True
    screen.fill((0,0,0))
    print('\tGame Over\n')
    message_display('Game Over', largetext, scrwidth/2, scrheight/2 - 25)
    message_display(reason, med_ocrfont, scrwidth/2, scrheight/2 + 25)

    ng_btn = Button('New Game', scrwidth/2, scrheight*0.75)

    pygame.display.update()

    # To allow the window to be closed even after the main gameloop has been exited
    while not ng_btn.clicked :
        for event in pygame.event.get():
                # If window is closed
                if event.type == pygame.QUIT :
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN :
                    if event.pos[0] in range(int(ng_btn.x - ng_btn.width/2), int(ng_btn.x + ng_btn.width/2)) and \
                       event.pos[1] in range(int(ng_btn.y - ng_btn.height/2), int(ng_btn.y + ng_btn.height/2)) :
                            newgame()

def newgame():
    """Begins a game"""
    global score, high_score
    if score > high_score :
        high_score = score
    saved_high = high_score
    
    pygame.display.quit()
    setup()
    high_score = saved_high
    gameloop()    
        
                

if __name__ == '__main__' :

    # Initialize pygame
    pygame.init()

    load_fonts()
    # Display the start screen
    start_screen()

    # Run the game
    setup()
    gameloop()
            
#_______________________________________________________________________________________________________________________

