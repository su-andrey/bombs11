import os
import random
import pygame

coords = []
all_sprites = pygame.sprite.Group()
class Bomb():
    def __init__(self):
        self.coords = []
        for _ in range(20):
            sprite = pygame.sprite.Sprite()
            sprite.image = self.load_image("bomb.png")
            sprite.rect = sprite.image.get_rect()
            sprite.rect.x = x
            sprite.rect.y = y
            coords.append(sprite.rect)
            all_sprites.add(sprite)

    def render(self, pos):
        for i in range(20):
            if coords[i].collidepoint(pos):
                sprite = pygame.sprite.Sprite()
                sprite.image = self.load_image("boom.png")
                sprite.rect = sprite.image.get_rect()
                sprite.rect.x = coords[i][0]
                sprite.rect.y = coords[i][1]
                coords.append(sprite.rect)
                all_sprites.add(sprite)


    def load_image(self, name):
        fullname = os.path.join('data', name)
        # если файл не существует, то выходим
        if not os.path.isfile(fullname):
            print(f"Файл с изображением '{fullname}' не найден")
            exit()
        image = pygame.image.load(fullname)
        return image

    def run(self):
        for i in range(20):
            coords[i][0], coords[i][1] = random.randint(0, 450), random.randint(0, 450)


if __name__ == '__main__':
    pygame.init()
    size = 500, 500
    x, y = 150, 150
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Бомбочки')
    bomb = Bomb()
    running = True
    clock = pygame.time.Clock()
    while running:
        clock.tick(10)
        bomb.run()
        screen.fill('black')
        all_sprites.draw(screen)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                bomb.render(event.pos)


