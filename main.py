import pygame
import random
import sys

FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((0, 0), 1)
pygame.display.set_caption("NeonNitro")
clock = pygame.time.Clock()
menu = pygame.transform.scale(pygame.image.load('date/menu_screen.png'), (1920, 1080))
game = pygame.Surface((1920, 1080))
settings = pygame.transform.scale(pygame.image.load('date/settings_screen.png'), (1920, 1080))
now_screen = menu
all_sprites = pygame.sprite.Group()


class Car(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)


class Field(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.image = pygame.transform.scale(pygame.image.load('date/field.png'), (1920, 1080))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0


field = Field()
running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if now_screen == menu:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 830 < event.pos[0] < 1090 and 540 < event.pos[1] < 610 and event.button == 1:
                    now_screen = game
                if 410 < event.pos[0] < 610 and 790 < event.pos[1] < 860 and event.button == 1:
                    running = False
                if 1340 < event.pos[0] < 1520 and 190 < event.pos[1] < 370 and event.button == 1:
                    now_screen = settings
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    now_screen = menu
        all_sprites.update(event)
    screen.fill((0, 0, 0))
    all_sprites.draw(game)
    screen.blit(now_screen, (0, 0))
    pygame.display.flip()

pygame.quit()
