from tkinter.messagebox import NO
from typing import Tuple
import pygame, sys
import random 

#General setup
pygame.init()
clock = pygame.time.Clock()
game_font = pygame.font.Font("freesansbold.ttf",32)
score_point = 1

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
        self.draw = pygame.Rect(screen_width/2 - 7,screen_height/2 - 7,15,15)
        self.color = bg_color
        self.baseSpeed = 10
        self.speed_x = self.baseSpeed 
        self.speed_y = self.baseSpeed 
        self.out_position = 0

    def selfDraw(self):
        pygame.draw.rect(screen,light_grey,self.draw)

    def restart(self):
        self.out_position = self.draw.left 
        self.draw.center = (screen_width/2,screen_height/2)
        pygame.draw.aaline(screen,light_grey,(screen_width/2,0),(screen_width/2,screen_height))
        
        self.speed_x = 0
        self.speed_y = 0

    def animation(self):
        #ball movement
        self.draw.x += self.speed_x
        self.draw.y += self.speed_y

        if self.draw.top <= 0 or self.draw.bottom >= screen_height:
            self.speed_y*=-1
        if self.draw.left <= 0 or self.draw.left >= screen_width:
            self.restart()
            
        if self.draw.colliderect(player.draw):
            self.speed_y = 8
            if abs(self.draw.top - player.draw.bottom) < 10 and self.speed_y > 0:
                self.speed_x*= -1
                self.speed_y*= random.choice((1.5,1,-1.5)) 
                
            if abs(self.draw.bottom - player.draw.top) < 10 and self.speed_y < 0:
                #print("ok 2.1")
                self.speed_x*= -1
                
            if abs(self.draw.right - player.draw.left) < 11 and self.speed_x > 0 or abs(self.draw.left - player.draw.right) < 10 and self.speed_x > 0:
                #print("ok 3.1")
                self.speed_x*= -1
                self.speed_y*= random.choice((1.5,1,-1.5))

        if self.draw.colliderect(opponent.draw):
            self.speed_y = 8
            #print ("1 collision ", abs(self.draw.top - opponent.draw.bottom) )
            #print ("2 collision ", abs(self.draw.bottom - opponent.draw.top) )
            #print ("3 collision ", abs(self.draw.right - opponent.draw.left) )
            #print ("c speed ", self.speed_y )

            if abs(self.draw.top - opponent.draw.bottom) < 10 and self.speed_y > 0:
                self.speed_y*= random.choice((1.5,1,-1.5)) 
                self.speed_x*= -1
                #print("ok 1")

            if abs(self.draw.bottom - opponent.draw.top) < 10 and self.speed_y < 0:
                #self.speed_y*= random.choice((1.5,1,-1.5)) 
                self.speed_x*= random.choice((1.5,1,-1.5)) 
                #print("ok 2")

            if abs(self.draw.right - opponent.draw.left) < 10 and self.speed_x < 0:
                self.speed_y*= random.choice((1.5,1,-1.5)) 
                self.speed_x*= -1
                #print("ok 3")
            
            #print ("self.speed_y ", self.speed_y )
            
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
        self.speed -= 10

    def move_down(self):
        self.speed += 10

    def ai_activated(self,y_axys):
        
        self.speed = 10

        if (round(pygame.time.get_ticks()) % 300) == 0:
            self.random = random.randint(5, 10)

        if self.draw.top <= 10:
           self.draw.top = 10
        if self.draw.bottom >= screen_height - 10:
           self.draw.bottom = screen_height - 10

        if self.draw.top + self.random <= y_axys - 50:
            self.draw.y += self.speed
        if self.draw.bottom - self.random >= y_axys + 50:
            self.draw.y -= self.speed

def restart(player,opponent,ball):
    player.draw = pygame.Rect(screen_width - 30,screen_height/2 - 70,10,140)
    opponent.draw = pygame.Rect(30,screen_height/2 - 70,10,140)
    ball.animation()
    pass

#Checkout how to inherit Player into a new class             

#game rectangles / objects
ball = scuareBall()
player = Player()
opponent = Player()
player.draw = pygame.Rect(screen_width - 30,screen_height/2 - 70,10,140)
opponent.draw = pygame.Rect(30,screen_height/2 - 70,10,140)

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
    
    player.animation()
    opponent.ai_activated(ball.draw.y)

    ##print(opponent.speed)
    if ball.out_position >= screen_width:
        opponent.score += 1
        score_point  = pygame.time.get_ticks()
    elif ball.out_position < 0:
        player.score += 1
        score_point  = pygame.time.get_ticks()
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
    pygame.draw.rect(screen,light_grey,(screen_width/2 - 50,screen_height/2 - 50,100,100),1)
    pygame.draw.aaline(screen,light_grey,(screen_width/2,0),(screen_width/2,screen_height))

    if score_point:
        counter = 3
        
        if pygame.time.get_ticks() - score_point < 700:
            pygame.draw.rect(screen,light_grey,(screen_width/2 - 25,screen_height/2 + 50,50,50),0)
            screen.blit(game_font.render(f"{counter}",False,bg_color),(screen_width/2 - 8, screen_height/2 + 60))

        if pygame.time.get_ticks() - score_point < 1400 and pygame.time.get_ticks() - score_point > 700:
            pygame.draw.rect(screen,light_grey,(screen_width/2 - 25,screen_height/2 + 50,50,50),0)
            screen.blit(game_font.render(f"{counter - 1}",False,bg_color),(screen_width/2 - 8, screen_height/2 + 60))

        if pygame.time.get_ticks() - score_point > 1400:
            pygame.draw.rect(screen,light_grey,(screen_width/2 - 25,screen_height/2 + 50,50,50),0)
            screen.blit(game_font.render(f"{counter - 2}",False,bg_color),(screen_width/2 - 8, screen_height/2 + 60))
            
        if pygame.time.get_ticks() - score_point > 2100:
            ball.speed_x = ball.baseSpeed * random.choice([1,-1])
            ball.speed_y = ball.baseSpeed * random.choice([1,-1])
            score_point = None
    else:
        ball.animation()
        
    pygame.display.flip()
    clock.tick(60)
    
    #print(round(pygame.time.get_ticks()))