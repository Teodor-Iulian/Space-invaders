import pygame
import random
import math
import time
import sys
from pygame import mixer


class Button():
    def __init__(self, image, pos, text_input, font, base_color, hovering_color):
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                          self.rect.bottom):
            return True
        return False

    def changeColor(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                          self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)


pygame.init()

screen_width = 1600
screen_height = 900
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Menu")

BG = pygame.image.load("assets/Background.png")


def get_font(size):  # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)


def play():
    while True:
        pygame.display.set_caption("Space Invaders")
        score_val = 0
        PLAY_MOUSE_POS = pygame.mouse.get_pos()
        screen.fill("black")

        # Score
        score_val = 0
        scoreX = 5
        scoreY = 5
        font = pygame.font.Font('freesansbold.ttf', 20)

        # Game Over
        game_over_font = pygame.font.Font('freesansbold.ttf', 64)

        def show_score(x, y):
            score = font.render("Points: " + str(score_val),
                                True, (255, 255, 255))
            screen.blit(score, (x, y))

        def game_over():
            game_over_text = game_over_font.render("GAME OVER",
                                                   True, (255, 255, 255))
            screen.blit(game_over_text, (590, 390))

        # Background Sound
        mixer.music.load('data/background.mp3')
        mixer.music.play(-1)

        # player
        playerImage = pygame.image.load('data/spaceship.png')
        player_X = 800
        player_Y = 800
        player_Xchange = 0

        # Invader
        invaderImage = []
        invader_X = []
        invader_Y = []
        invader_Xchange = []
        invader_Ychange = []
        no_of_invaders = 16

        for num in range(no_of_invaders):
            invaderImage.append(pygame.image.load('data/alien.png'))
            invader_X.append(random.randint(64, 1500))
            invader_Y.append(45)
            invader_Xchange.append(1.2)
            invader_Ychange.append(50)

        # Bullet
        bulletImage = pygame.image.load('data/bullet.png')
        bullet_X = 0
        bullet_Y = 800
        bullet_Xchange = 0
        bullet_Ychange = 3
        bullet_state = "rest"

        # Collision Concept
        def isCollision(x1, x2, y1, y2):
            distance = math.sqrt((math.pow(x1 - x2, 2)) + (math.pow(y1 - y2, 2)))
            if distance <= 50:
                return True
            else:
                return False

        def player(x, y):
            screen.blit(playerImage, (x - 16, y + 10))

        def invader(x, y, i):
            screen.blit(invaderImage[i], (x, y))

        def bullet(x, y):
            global bullet_state
            screen.blit(bulletImage, (x, y))

        explosion_sound = mixer.Sound('data/explosion.wav')

        # Initialize a flag to track game over state
        game_over_flag = False

        # game loop
        running = True
        while running:

            # RGB
            screen.fill((0, 0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # Instead of quitting, go back to the menu
                    pygame.display.set_caption("Menu")
                    pygame.mixer.music.stop()
                    score_val=0
                    main_menu()

                # Controlling the player movement
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        player_Xchange = -1.7
                    if event.key == pygame.K_RIGHT:
                        player_Xchange = 1.7
                    if event.key == pygame.K_SPACE:
                        # Fire the bullet
                        if bullet_state == "rest":
                            bullet_X = player_X
                            bullet_Y = player_Y  # Start the bullet from player's position
                            bullet_state = "fire"
                            bullet_sound = mixer.Sound('data/bullet.mp3')
                            bullet_sound.play()

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        player_Xchange = 0


            # Update the player position
            player_X += player_Xchange

            # Update the invader positions
            for i in range(no_of_invaders):
                invader_X[i] += invader_Xchange[i]

            # Bullet movement
            if bullet_Y <= 0:
                bullet_Y = 800
                bullet_state = "rest"
            if bullet_state == "fire":
                bullet(bullet_X, bullet_Y)
                bullet_Y -= bullet_Ychange  # Move bullet upwards

            # Invader movement
            for i in range(no_of_invaders):

                if invader_Y[i] >= 750:
                    if abs(player_X - invader_X[i]) < 40:
                        for j in range(no_of_invaders):
                            invader_Y[j] = 2000
                        mixer.music.stop()

                        if not game_over_flag:
                            explosion_sound.play()
                            game_over_flag = True

                        game_over()
                        break

                if invader_X[i] >= 1535 or invader_X[i] <= 0:
                    invader_Xchange[i] *= -1
                    invader_Y[i] += invader_Ychange[i]

                # Collision detection
                collision = isCollision(bullet_X, invader_X[i], bullet_Y, invader_Y[i])
                if collision:
                    score_val += 1
                    bullet_Y = 800
                    bullet_state = "rest"
                    invader_X[i] = random.randint(64, 1500)
                    invader_Y[i] = 45
                    invader_Xchange[i] *= -1

                invader(invader_X[i], invader_Y[i], i)

            # Restrict player movement within the screen
            if player_X <= 16:
                player_X = 16
            elif player_X >= 1584:
                player_X = 1584

            player(player_X, player_Y)
            show_score(scoreX, scoreY)
            pygame.display.update()


def main_menu():
    while True:
        screen.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(800, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(800, 250),
                             text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(800, 450),
                             text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        screen.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Go back to the main menu instead of quitting the game
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


main_menu()
