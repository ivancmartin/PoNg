from pongPlayer import Player
from pongBall import scuareBall
import pygame, sys

pygame.init()
clock = pygame.time.Clock()
timer = int (0)
game_font = pygame.font.Font("freesansbold.ttf",32)
score_point = 1

#setting up the main window
screen_width = 920
screen_height = 740

screen = pygame.display.set_mode((screen_width,screen_height),vsync=1)
pygame.display.set_caption('Pong')

bg_color = (50,50,50)
light_grey = (200,200,200)

player = Player('player')
player.draw = pygame.Rect(screen_width - 35,screen_height/2 - 70,10,140)
player.movement_limit['y'] = screen_height

bot = Player('bot')
bot.draw = pygame.Rect(35,screen_height/2 - 70,10,140)
bot.movement_limit['y'] = screen_height

ball = scuareBall('scuareBall')
ball.draw = pygame.Rect(screen_width/2 - 7,screen_height/2 - 7,15,15)
ball.movement_limit = {'x': screen_width, 'y' : screen_height}

while True:
    objects = [player,ball,bot]
    screen.fill(bg_color)
    player.selfDraw(screen)
    bot.selfDraw(screen)
    bot.color = (200,150,200)
    ball.selfDraw(screen)
    
    if round(pygame.time.get_ticks()) > timer + 5000:
        ball.accelerate()
        bot.accelerate()
        player.accelerate()
        timer = round(pygame.time.get_ticks()) 

    keys = pygame.key.get_pressed()
    # Handling input

    #player 1 score (right)
    if player.score >= 10:
        screen.blit(game_font.render(f"{player.score}",False,light_grey),(screen_width/2 + 15, 30))
    else:
        screen.blit(game_font.render(f"{player.score}",False,light_grey),(screen_width/2 + 15, 30))

    #player 2 score (right)
    if bot.score >= 10:
        screen.blit(game_font.render(f"{bot.score}",False,light_grey),(screen_width/2 - 45, 30))
    else:
        screen.blit(game_font.render(f"{bot.score}",False,light_grey),(screen_width/2 - 30, 30))

    pygame.draw.rect(screen,light_grey,(screen_width/2 - 50,screen_height/2 - 50,100,100),1)
    pygame.draw.aaline(screen,light_grey,(screen_width/2,0),(screen_width/2,screen_height))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    #movement
    player._process()
    bot._process()
    ball._process()
    bot.auto_move(ball.draw.y)
    ball.selfCheckColision(objects)

    if keys[pygame.K_DOWN] or keys[pygame.K_UP]:
        player.new_state = 'run'
        bot.new_state = 'run'
        player.current_direction = (keys[pygame.K_DOWN] - keys[pygame.K_UP])
        bot.current_direction = (keys[pygame.K_DOWN] - keys[pygame.K_UP])
    else:
        player.new_state = 'idle'
        bot.new_state = 'idle'
    
    ball.new_state = 'run'

    if ball.out_position >= screen_width:
        bot.score += 1
        score_point = pygame.time.get_ticks()
      
    elif ball.out_position < 0:
        player.score += 1
        score_point = pygame.time.get_ticks()

    ball.out_position = 0

    if score_point:
        player.reset_position({'x': screen_width, 'y' : screen_height/2})
        bot.reset_position({'x': screen_width, 'y' : screen_height/2})
        player.move(False)
        bot.move(False)
        ball.new_state = 'idle'
        #bot.resetSpeed()
        #player.resetSpeed()

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
            score_point = None
            player.move(True)
            bot.move(True)
    else:
        ball.new_state = 'run'
       
    pygame.display.flip()
    clock.tick(60)