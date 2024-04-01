import math
import random
import os
import pathlib
PATH = pathlib.Path(__file__).parent.resolve()
os.chdir(PATH)
import pygame
# For musikk
from pygame import mixer 

class Scoreboard:
    def __init__(self, score_value, font):
        self.score_value = score_value
        self.font = font

    def show_score(self, screen, x, y):
        score = self.font.render("Score : " + str(self.score_value), True, (255, 255, 255))
        screen.blit(score, (x, y))

class GameOverText:
    def __init__(self, over_font):
        self.over_font = over_font

    def show_game_over(self, screen):
        over_text = self.over_font.render("GAME OVER", True, (255, 255, 255))
        screen.blit(over_text, (200, 250))

class Player:
    def __init__(self, image, x, y):
        self.image = image
        self.x = x
        self.y = y
        self.x_change = 0

    def move_left(self):
        self.x_change = -5

    def move_right(self):
        self.x_change = 5

    def stop(self):
        self.x_change = 0

    def update_position(self):
        self.x += self.x_change
        if self.x <= 0:
            self.x = 0
        elif self.x >= 736:
            self.x = 736

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

class Enemy:
    def __init__(self, image, x, y, x_change, y_change):
        self.image = image
        self.x = x
        self.y = y
        self.x_change = x_change
        self.y_change = y_change

    def update_position(self):
        self.x += self.x_change
        if self.x <= 0:
            self.x_change = 4
            self.y += self.y_change
        elif self.x >= 736:
            self.x_change = -4
            self.y += self.y_change

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def collide(self, x, y, bullet_x, bullet_y):
        distance = math.sqrt((self.x - bullet_x) ** 2 + (self.y - bullet_y) ** 2)
        return distance < 27

class Bullet:
    def __init__(self, image, x, y, y_change):
        self.image = image
        self.x = x
        self.y = y
        self.y_change = y_change
        self.state = "ready"

    def fire(self, x, y):
        if self.state == "ready":
            self.state = "fire"
            self.x = x

    def update_position(self):
        if self.state == "fire":
            self.y -= self.y_change
            if self.y <= 0:
                self.state = "ready"
                self.y = 480  # Tilbakestill y-posisjonen til spillerens posisjon

    def draw(self, screen):
        if self.state == "fire":
            screen.blit(self.image, (self.x + 16, self.y + 10))


pygame.init()
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('background.png')

# Sound
mixer.music.load("background.wav")
mixer.music.play(-1)

# Caption and Icon
pygame.display.set_caption("Space Invader")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0
player = Player(playerImg, playerX, playerY)

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6
enemies = []  # Liste til å holde Enemy objekter

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)
    enemies.append(Enemy(enemyImg[i], enemyX[i], enemyY[i], enemyX_change[i], enemyY_change[i]))

# Bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletY_change = 10
bullet = Bullet(bulletImg, bulletX, bulletY, bulletY_change)

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
testY = 10
scoreboard = Scoreboard(score_value, font)

# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)
game_over_text = GameOverText(over_font)

running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.move_left()
            if event.key == pygame.K_RIGHT:
                player.move_right()
            if event.key == pygame.K_SPACE:
                bullet.fire(player.x, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player.stop()

    player.update_position()
    bullet.update_position()

    for enemy in enemies:
        if enemy.y > 440:
            for e in enemies:
                e.y = 2000
            game_over_text.show_game_over(screen)
            break

        enemy.update_position()

        if enemy.collide(enemy.x, enemy.y, bullet.x, bullet.y):
            explosionSound = mixer.Sound("explosion.wav")
            explosionSound.play()
            bullet.y = 480
            bullet.state = "ready"
            scoreboard.score_value += 1
            enemy.x = random.randint(0, 736)
            enemy.y = random.randint(50, 150)

        enemy.draw(screen)

    if bullet.y <= 0:
        bullet.y = 480
        bullet.state = "ready"

    if bullet.state == "fire":
        bullet.draw(screen)
        bulletY -= bulletY_change

    player.draw(screen)
    scoreboard.show_score(screen, textX, testY)
    pygame.display.update()
