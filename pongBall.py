from typing import Tuple
from stateMachine import StateMachine
from pongPlayer import Player
import pygame
import random 

class scuareBall(StateMachine):
    #att
    draw : pygame.Rect
    color: Tuple
    base_speed : int
    direction_x : int 
    direction_y : int
    out_position : int
    acceleration : int
    movement_limit : dict

    def __init__(self,name):
        StateMachine.__init__(self,name)

        self.movement_limit = {'y' : 0, 'x' : 0}
        self.color = (200,200,200)
        self.base_speed = 5
        self.acceleration = 1
        self.direction_x = random.choice([1,-1])
        self.direction_y = random.choice([1,-1])
        self.out_position = 0
        self.colide_with_player = False

    def _idle(self):
        print('im a ball stoped!')

    def _run(self):
        #ball movement
        self.draw.x += (self.base_speed) * self.direction_x
        self.draw.y += (self.base_speed) * self.direction_y
        
        if self.draw.top <= 0 or self.draw.bottom >= self.movement_limit['y']:
            self.direction_y*=-1
            self.colide_with_player = False
            
        if self.draw.left <= 0 or self.draw.left >= self.movement_limit['x']:
            #self.direction_x*=-1
            self.restart()

    def selfDraw(self,screen):
        pygame.draw.rect(screen,self.color,self.draw)
    
    def selfCheckColision(self,objects:list):
        for obj in objects:
            if type(obj) == Player and not self.colide_with_player:
                if self.draw.colliderect(obj.draw):
                    self.colide_with_player = True
                    self.direction_x*= -1
 
    def restart(self):
        self.out_position = self.draw.left
        self.draw.center = (self.movement_limit['x']/2,self.movement_limit['y']/2)
        self.acceleration = 1
        self.direction_x = random.choice([1,-1])
        self.direction_y = random.choice([1,-1])
        self.colide_with_player = False
    
    def accelerate(self):
        self.base_speed += 0.5