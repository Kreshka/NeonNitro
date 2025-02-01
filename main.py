import pygame
import random
import sys

FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

W, H = 1920, 1080

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((0, 0), 1)
pygame.display.set_caption("NeonNitro")
clock = pygame.time.Clock()
menu = pygame.transform.scale(pygame.image.load('date/menu_screen.png'), (W, H))
game = pygame.Surface((W, H))
settings = pygame.transform.scale(pygame.image.load('date/settings_screen.png'), (W, H))
now_screen = menu
all_sprites = pygame.sprite.Group()
cars = pygame.sprite.Group()
xs = []


class Car(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(cars)
        self.image = pygame.transform.scale(pygame.image.load('date/main_car.png'), (133, 245))
        self.rect = self.image.get_rect()
        self.rect.x = 500
        self.rect.y = 740


class MainCar(Car):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('date/main_car.png')
        self.s = 25

    def update(self, *args, **kwargs):
        g = pygame.key.get_pressed()
        if g[pygame.K_d] or g[pygame.K_RIGHT]:
            self.rect.x += self.s
        elif g[pygame.K_a] or g[pygame.K_LEFT]:
            self.rect.x -= self.s


class WCar(Car):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('date/d_car1.png')
        self.s = random.randint(40, 50)
        self.rect.x = random.randint(280, 1600)
        self.rect.y = random.randint(-7000, -2000)
        while len(pygame.sprite.spritecollide(self, cars, dokill=0)) > 1:
            self.rect.x = random.randint(280, 1600)
            self.rect.y = random.randint(-7000, -2000)
        xs.append(self.rect.x)

    def update(self, *args, **kwargs):
        self.rect.y += self.s
        if len(pygame.sprite.spritecollide(self, cars, dokill=0)) > 1:
            self.kill()
            dcars.append(WCar())
        if self.rect.y >= 1080:
            self.rect.y = -1000
            self.rect.x = random.randint(280, 1600)


class Field(pygame.sprite.Sprite):
    image = pygame.transform.scale(pygame.image.load('date/road.png'), (W, H))

    def __init__(self, p):
        super().__init__(all_sprites)
        self.image = Field.image
        self.rect = self.image.get_rect()
        self.rect.x = 0
        if p:
            self.rect.y = 0
        else:
            self.rect.y = -1080

    def update(self, *args, **kwargs):
        self.rect.y += 18
        if self.rect.y >= 1080:
            self.rect.y = -1080


p = 0
p2 = 0
running = True
while running:
    if now_screen == game and p == 0:
        field = Field(1)
        field2 = Field(0)
        car = MainCar()
        dcars = [WCar() for i in range(5)]
        p = 1
        p2 = 1
    if now_screen == menu and p2 == 1:
        field.kill()
        field2.kill()
        car.kill()
        dcars = list(map(lambda x: x.kill(), dcars))
        p2 = 0
        p = 0
    clock.tick(60)
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
    screen.fill((0, 0, 0))
    game.fill((0, 0, 0))
    all_sprites.update()
    all_sprites.draw(game)
    cars.update()
    cars.draw(game)
    screen.blit(now_screen, (0, 0))
    pygame.display.flip()

pygame.quit()
