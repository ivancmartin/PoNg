from typing import Tuple
import pygame, sys
import random 

#General setup
pygame.init()
clock = pygame.time.Clock()
game_font = pygame.font.Font("freesansbold.ttf",32)

#setting up the main window
screen_width = 1280
screen_height = 930
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('Pong')

#colors
#bg_color = pygame.Color('grey12')
bg_color = (50,50,50)
light_grey = (200,200,200)

#objets
#scuareBall -> tha ball
class scuareBall:
    #att
    draw : pygame.Rect
    color: Tuple
    baseSpeed : int
    speed_x : int 
    speed_y : int
    out_position : int

    def __init__(self):
        self.draw = pygame.Rect(screen_width/2 - 15,screen_height/2 - 15,30,30)
        self.color = bg_color
        self.baseSpeed = 7
        self.speed_x = self.baseSpeed 
        self.speed_y = self.baseSpeed 
        self.out_position = 0

    def selfDraw(self):
        pygame.draw.rect(screen,light_grey,self.draw)

    def restart(self):
        import random
        self.out_position = self.draw.left 
        self.speed_x = self.baseSpeed * random.choice([1,-1])
        self.draw.center = (screen_width/2,screen_height/2)

    def animation(self):
        #ball movement
        self.draw.x += self.speed_x
        self.draw.y += self.speed_y

        if self.draw.top <= 0 or self.draw.bottom >= screen_height:
            self.speed_y*=-1
        if self.draw.left <= 0 or self.draw.left >= screen_width:
            self.restart()
            
        if self.draw.colliderect(player.draw) or self.draw.colliderect(opponent.draw):
            self.speed_x*=-1
            self.speed_y*= random.choice((-1, 1))
            
class Player:
    #att
    draw : pygame.Rect
    color: Tuple
    speed : int
    socre : int
    random: int

    def __init__(self):
        #self.draw = pygame.Rect(screen_width - 25,screen_height/2 - 70,10,140)
        self.color = bg_color
        self.speed = 0
        self.score = 0
        self.random = 0

    def selfDraw(self):
        pygame.draw.rect(screen,light_grey,self.draw)

    def animation(self):
        self.draw.y += self.speed
        
        if self.draw.top <= 10:
           self.draw.top = 10
        if self.draw.bottom >= screen_height - 10:
            self.draw.bottom = screen_height - 10

    def move_up(self):
        self.speed -= 7

    def move_down(self):
        self.speed += 7

    def ai_activated(self,y_axys):
        
        if (round(pygame.time.get_ticks()) % 300) == 0:
            self.random = random.randint(5, 10)

        if self.draw.top <= 10:
           self.draw.top = 10
        if self.draw.bottom >= screen_height - 10:
           self.draw.bottom = screen_height - 10

        if self.draw.top + self.random <= y_axys:
            self.draw.y += self.speed
        if self.draw.bottom - self.random >= y_axys:
            self.draw.y -= self.speed

#Checkout how to inherit Player into a new class             

#game rectangles / objects
ball = scuareBall()
player = Player()
opponent = Player()
player.draw = pygame.Rect(screen_width - 30,screen_height/2 - 70,10,140)
opponent.draw = pygame.Rect(15,screen_height/2 - 70,10,140)
opponent.speed = 7

while True:
    # Handling input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        #imputs
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                player.move_down()
            if event.key == pygame.K_UP:
                player.move_up()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                player.move_up()
            if event.key == pygame.K_UP:
                player.move_down()
    
    #movement
    ball.animation()
    player.animation()
    opponent.ai_activated(ball.draw.y)

    ##print(opponent.speed)
    if ball.out_position >= screen_width:
        opponent.score += 1
    elif ball.out_position < 0:
        player.score += 1
    ball.out_position = 0

    #Visual Elements
    screen.fill(bg_color)
    ball.selfDraw()
    player.selfDraw()
    opponent.selfDraw()
    
    #player 1 score (right)
    screen.blit(game_font.render(f"{player.score}",False,light_grey),(screen_width/2 + 15, 30))
   
    #player 2 score (right)
    screen.blit(game_font.render(f"{opponent.score}",False,light_grey),(screen_width/2 - 30, 30))

    #line drawed
    pygame.draw.aaline(screen,light_grey,(screen_width/2,0),(screen_width/2,screen_height))
    pygame.draw.rect(screen,light_grey,(screen_width/2 - 50,screen_height/2 - 50,100,100),1)
    pygame.display.flip()
    clock.tick(60)
    
    #print(clock.get_fps())
    print(round(pygame.time.get_ticks()))