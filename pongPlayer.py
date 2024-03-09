from typing import Tuple
import pygame
from stateMachine import StateMachine
import random

class Player(StateMachine):
    #att
    draw : pygame.Rect
    color: Tuple
    base_speed : int = 10
    speed : int
    score : int
    random: int
    acceleration : int
    can_move: bool
    movement_limit : dict
    current_direction : int
    auto_move_accuracy : int

    def __init__(self,name):
        StateMachine.__init__(self,name)
        
        #self.draw = pygame.Rect(screen_width - 25,screen_height/2 - 70,10,140)
        self.color = (200,200,200)
        self.speed = 10
        self.score = 0
        self.acceleration = 0
        self.can_move = True
        self.movement_limit = {'y' : 0, 'x' : 0}
        self.current_direction = 0
        self.auto_move_accuracy = 0
    
    def _idle(self):
        self.current_direction = 0

    def _run(self):
        if self.can_move:
            self.draw.y += (self.current_direction * self.speed)

            if self.draw.top < 10:
                self.draw.top = 1
            
            if self.draw.bottom > self.movement_limit['y'] - 10:
                self.draw.bottom = self.movement_limit['y'] - 1

    def selfDraw(self,screen):
        pygame.draw.rect(screen,self.color,self.draw)
    
    def changeColor(self,newColor : Tuple):
        self.color = newColor

    def move(self, val : bool):
        self.can_move = val

    def accelerate(self):
        self.speed += 0.1

    def auto_move(self, position):
        if self.can_move:
            #self.speed = 10 + self.acceleration

            if self.draw.top < 10:
                self.draw.top = 1
            
            if self.draw.bottom > self.movement_limit['y'] - 10:
                self.draw.bottom = self.movement_limit['y'] - 1

            if (round(pygame.time.get_ticks()) % 300) == 0:
                self.auto_move_accuracy = random.randint(-15, -5)

            print(self.auto_move_accuracy)

            if self.draw.top + self.auto_move_accuracy <= position - 50:
                self.draw.y += self.speed
                
            if self.draw.bottom - self.auto_move_accuracy >= position + 50:
                self.draw.y -= self.speed

    def reset_position(self, position):
        if (self.draw.top) < (position['y'] - self.draw.height/2):
            self.draw.y += self.speed
        
        elif (self.draw.top) > (position['y'] - self.draw.height/2):
            self.draw.y -= self.speed
    

    '''
    def resetSpeed(self):
        self.speed = self.base_speed
    '''