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
menu = pygame.transform.scale(pygame.image.load('data/menu_screen.png'), (W, H))
game = pygame.Surface((W, H))
settings = pygame.transform.scale(pygame.image.load('data/settings_screen.png'), (W, H))
game_over = pygame.transform.scale(pygame.image.load('data/game_over_screen.png'), (W, H))
n1, n2, n3, go = (
    pygame.transform.scale(pygame.image.load('data/number1.png'), (W, H)),
    pygame.transform.scale(pygame.image.load('data/number2.png'), (W, H)),
    pygame.transform.scale(pygame.image.load('data/number3.png'), (W, H)),
    pygame.transform.scale(pygame.image.load('data/GO!_screen.png'), (W, H)),
)
now_screen = menu
all_sprites = pygame.sprite.Group()
game_over_group = pygame.sprite.Group()
start_nums_group = pygame.sprite.Group()
cars = pygame.sprite.Group()
xs = []


class Car(pygame.sprite.Sprite):
    def __init__(self, cl):
        super().__init__(cl)
        self.image = pygame.transform.scale(pygame.image.load('data/main_car.png'), (133, 245))
        self.rect = self.image.get_rect()
        self.rect.x = 500
        self.rect.y = 740


class MainCar(Car):
    def __init__(self):
        super().__init__(all_sprites)
        self.image = pygame.image.load('data/main_car.png')
        self.s = 25

    def update(self, *args, **kwargs):
        global now_screen, game_running, game_over_flag
        if not game_over_flag:
            g = pygame.key.get_pressed()
            if g[pygame.K_d] or g[pygame.K_RIGHT]:
                self.rect.x += self.s
            elif g[pygame.K_a] or g[pygame.K_LEFT]:
                self.rect.x -= self.s
            if pygame.sprite.spritecollide(self, cars, dokill=1):
                game_over_flag = True
            if self.rect.x <= 180:
                self.rect.x += self.s
            if self.rect.x >= 1750 - self.rect.w:
                self.rect.x -= self.s
        else:
            pass


class WCar(Car):
    def __init__(self):
        super().__init__(cars)
        self.image = pygame.image.load('data/d_car1.png')
        self.s = random.randint(40, 50)
        self.rect.x = random.randint(280, 1600)
        self.rect.y = random.randint(-7000, -2000)
        while len(pygame.sprite.spritecollide(self, cars, dokill=0)) > 1:
            self.rect.x = random.randint(280, 1600)
            self.rect.y = random.randint(-7000, -2000)
        xs.append(self.rect.x)

    def update(self, *args, **kwargs):
        if not game_over_flag:
            self.rect.y += self.s
            if len(pygame.sprite.spritecollide(self, cars, dokill=0)) > 1:
                self.kill()
                dcars.append(WCar())
            if self.rect.y >= 1080:
                self.rect.y = -1000
                self.rect.x = random.randint(280, 1600)
        else:
            pass


class Field(pygame.sprite.Sprite):
    image = pygame.transform.scale(pygame.image.load('data/road.png'), (W, H))

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
        if not game_over_flag:
            self.rect.y += 18
            if self.rect.y >= 1080:
                self.rect.y = -1080


class GameOver(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(game_over_group)
        self.image = game_over
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = -1920
        self.s = 10

    def update(self, *args, **kwargs):
        if game_over_flag:
            if self.rect.y >= -self.s:
                self.rect.y = 0
                self.s = 0
            else:
                self.rect.y += self.s
                self.s += 10


class StartingGameNums(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(start_nums_group)
        self.images = [n3, n2, n1, go]
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.f = 1

    def update(self, *args, **kwargs):
        global starting_flag
        if self.f == 15:
            self.image = self.images[1]
        if self.f == 30:
            self.image = self.images[2]
        if self.f == 45:
            self.image = self.images[3]
        if self.f == 60:
            starting_flag = True
        self.f += 1


p = 0
p2 = 0
running = True
game_running = True
sets_running = True
game_over_flag = False
starting_flag = False
dcars = []


def game_loop():
    global now_screen, game_running, game_over_flag, starting_flag
    game_running = True
    game_over_flag = False
    starting_flag = False
    start_nums_obj = StartingGameNums()
    while not starting_flag:
        screen.fill((0, 0, 0))
        game.fill((0, 0, 0))
        start_nums_group.update()
        start_nums_group.draw(game)
        screen.blit(game, (0, 0))
        pygame.display.flip()
    field = Field(1)
    field2 = Field(0)
    car = MainCar()
    game_over_obj = GameOver()
    dcars = [WCar() for _ in range(5)]
    while game_running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE and game_over_flag:
                    game_running = False

        screen.fill((0, 0, 0))
        game.fill((0, 0, 0))
        all_sprites.update()
        all_sprites.draw(game)
        cars.update()
        cars.draw(game)
        game_over_group.update()
        game_over_group.draw(game)
        screen.blit(game, (0, 0))
        pygame.display.flip()
        clock.tick(60)
    field.kill()
    field2.kill()
    car.kill()
    game_over_obj.kill()
    start_nums_obj.kill()
    dcars = list(map(lambda x: x.kill(), dcars))


def skins_menu():
    global sets_running
    sets_running = True
    while sets_running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sets_running = False

        screen.fill((0, 0, 0))
        screen.blit(settings, (0, 0))
        pygame.display.flip()


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if 830 < event.pos[0] < 1090 and 540 < event.pos[1] < 610 and event.button == 1:
                game_loop()
            if 410 < event.pos[0] < 610 and 790 < event.pos[1] < 860 and event.button == 1:
                running = False
            if 1310 <= event.pos[0] <= 1590 and 270 <= event.pos[1] <= 340 and event.button == 1:
                skins_menu()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    screen.fill((0, 0, 0))
    screen.blit(menu, (0, 0))
    pygame.display.flip()

pygame.quit()
