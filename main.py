import os

import pygame

width, height = 500, 500
all_sprites = pygame.sprite.Group()
pygame.init()
size = 500, 500
x, y = 150, 150
screen = pygame.display.set_mode(size)
parachutes = pygame.sprite.Group()
pygame.display.set_caption('Парашют')


def load_image(name, colorkey=-1):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Mountain(pygame.sprite.Sprite):
    image = load_image("mountains.png")

    def __init__(self):
        super().__init__(all_sprites)
        self.image = Mountain.image
        self.rect = self.image.get_rect()
        # вычисляем маску для эффективного сравнения
        self.mask = pygame.mask.from_surface(self.image)
        # располагаем горы внизу
        self.rect.bottom = height

mountain = Mountain()

class Landing(pygame.sprite.Sprite):
    image = load_image("parachute.png")

    def __init__(self, pos):
        super().__init__(all_sprites)
        self.image = Landing.image
        self.rect = self.image.get_rect()
        # вычисляем маску для эффективного сравнения
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = pos[0] - 58
        self.rect.y = pos[1] - 50

    def update(self):
        # если ещё в небе
        if not pygame.sprite.collide_mask(self, mountain):
            self.rect = self.rect.move(0, 1)



running = True
clock = pygame.time.Clock()
while running:
    clock.tick(30)
    all_sprites.draw(screen)
    parachutes.draw(screen)
    parachutes.update()
    pygame.display.flip()
    screen.fill('black')
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            parachutes.add(Landing(event.pos))
