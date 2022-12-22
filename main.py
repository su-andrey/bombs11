import os

import pygame


name = input()
pygame.init()
size = width, height = 500, 500
screen = pygame.display.set_mode(size)


def load_image(name):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        exit()
    image = pygame.image.load(fullname)
    return image


sprite_group = pygame.sprite.Group()
mario = pygame.sprite.Group()

tile_image = {'wall': load_image('box.png'),
              'empty': load_image('grass.png')}

FPS = 30


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(sprite_group)
        self.image = tile_image[tile_type]
        self.rect = self.image.get_rect().move(
            width / 10 * pos_x, height / 10 * pos_y)


player_image = load_image('mar.png')


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(mario)
        self.image = player_image
        self.rect = self.image.get_rect().move(width / 10 * x + 10, height / 10 * y + 10)
        self.pos = (x, y)

    def move(self, x, y):
        self.pos = (x, y)
        center = self.rect.center
        self.rect = self.image.get_rect().move(width / 10 * x + 15, height / 10 * y + 10)


def load_level(filename):
    try:
        filename = "data/" + filename
        # читаем уровень, убирая символы перевода строки
        with open(filename, 'r') as mapFile:
            lmap = [line.strip() for line in mapFile]
        # и подсчитываем максимальную длину
        max_width = max(map(len, lmap))
        return list(map(lambda x: x.ljust(max_width, '.'), lmap))
    except FileNotFoundError:
        print('Что-то было введено неверно.')
        exit()

clock = pygame.time.Clock()


def start_screen():
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "Если в правилах несколько строк,",
                  "приходится выводить их построчно"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


def move(mar, dest):
    x, y = mar.pos[0], mar.pos[1]
    if dest == 0 and y > 0 and lmap[y - 1][x] != '#':
        mar.move(x, y - 1)
    elif dest == 1 and x < max_x - 1 and lmap[y][x + 1] != '#':
        mar.move(x + 1, y)
    elif dest == 2 and y < max_y - 1 and lmap[y + 1][x] != '#':
        mar.move(x, y + 1)
    elif dest == 3 and x > 0 and lmap[y][x - 1] != '!':
        mar.move(x - 1, y)


start_screen()
lmap = load_level(name)
if __name__ == '__main__':
    running = True
    hero, max_x, max_y = generate_level(lmap)
    while running:
        sprite_group.draw(screen)
        mario.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    move(hero, 0)
                if event.key == pygame.K_RIGHT:
                    move(hero, 1)
                if event.key == pygame.K_DOWN:
                    move(hero, 2)
                if event.key == pygame.K_LEFT:
                    move(hero, 3)
        pygame.display.flip()
