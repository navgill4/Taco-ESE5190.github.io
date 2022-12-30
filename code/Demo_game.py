#Demo game for ESE 5190 Final Project

# Import and initialize the pygame library
import pygame
import serial
import random
import sys
import os
import pygame.freetype

from pygame.locals import (RLEACCEL)
score = 0   
fruits = ["apple.png", "new_strawberry.png", "grape.png", "orange.png", "watermelon.png", "banana.png" ]
fruit_sel = random.randint(0, 5)
white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)
pygame.init()
pygame.font.init()
font = pygame.font.Font('freesansbold.ttf', 32)
score_text = 'score'+str((score))
text = font.render(score_text, True, (0,0,0), white)
textRect = text.get_rect()

enemy_missed = 0
# set the center of the rectangular object.
textRect.center = (50, 50)
SCREEN_WIDTH = 160*8
SCREEN_HEIGHT = 80*8

# Set up the drawing window
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
class Background():
    def __init__(self):
        super(Background, self).__init__()
        self.surf = pygame.image.load("forest_2.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(center=(80*8,40*8))
class Player(pygame.sprite.Sprite):
   def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("knife.png").convert()
        self.surf.set_colorkey((254, 254, 254), RLEACCEL)
        self.rect = self.surf.get_rect()

   def update(self, a, b):
        self.rect = self.surf.get_rect(
            center=(a,b)
        )
        

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load(fruits[fruit_sel]).convert()
        self.surf.set_colorkey((254, 254, 254), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(60, 1280),
                0
            )
        )
        self.speed = random.randint(10, 30)

    # Move the sprite based on speed
    # Remove the sprite when it passes the left edge of the screen
    def update(self):
        global enemy_missed
        self.rect.move_ip(0, self.speed)
        if self.rect.top >= SCREEN_HEIGHT:
            enemy_missed +=1 
            self.kill()
            
        

player = Player()
Background=Background()
player_sprite = pygame.sprite.GroupSingle()
player_sprite.add(player)

ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 1000)

enemy_sprites = pygame.sprite.Group()

flag = True
running = True
while running:

    with serial.Serial('/dev/tty.usbmodem21101', 115200, timeout=1) as ser:
        line = ser.readline()
        line_str = str(line)
        print(line_str)
        x = [int(x) for x in line_str.split() if x.isdigit()]
        print(x[0])
        print(x[1])
        x_game = (x[0]*8)
        y_game = ((160-x[1])*8)
        
        
        
    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        elif event.type == ADDENEMY:
            # Create the new enemy and add it to sprite groups
            new_enemy = Enemy()
            enemy_sprites.add(new_enemy)

    # Fill the background with white
    screen.fill((255, 255, 255))

    # Draw a solid blue circle in the center
    #pygame.draw.circle(scree (0, 255, 255), (y_game, x_game), 10)
    enemy_sprites.update()
    
    screen.blit(Background.surf, Background.rect)
    for entity in enemy_sprites:
        screen.blit(entity.surf, entity.rect)
    
    
    screen.blit(player.surf, (y_game, x_game))
    player.update(y_game, x_game)
    


    if  pygame.sprite.spritecollide(player, enemy_sprites, True):
        score += 1
        score_text = 'score: '+str((score))
        text = font.render(score_text, True, (0,0,0), white)
        print(score_text)
        enemy_sprites.update
    #if pygame.sprite.spritecollideany(player, all_sprites):
    # If so, then remove the player and stop the loop
    screen.blit(text, textRect)
    fruit_sel = random.randint(0, 5)
    
    if enemy_missed >= 3:
        pygame.QUIT
        pygame.quit()
    # print(score)
    # Flip the display
    pygame.display.flip()

    
    

# Done! Time to quit.
pygame.quit()