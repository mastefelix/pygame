import pygame as pg
from random import randint

# Инициализация Pygame
pg.init()

# Параметры экрана
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption("Halloween")

# Цвета
BLACK, WHITE, ORANGE, RED = (0, 0, 0), (255, 255, 255), (255, 165, 0), (255, 0, 0)

# Загрузка изображений
images = {
    'player': pg.image.load('images/pumpkin.png'),
    'candy': pg.image.load('images/candy.png'),
    'ghost': pg.image.load('images/ghost.png'),
    'background': pg.transform.scale(pg.image.load('images/bg_halloween_2.jpg'), (SCREEN_WIDTH, SCREEN_HEIGHT))
}

# Размеры объектов
PLAYER_SIZE, CANDY_SIZE, GHOST_SIZE = (50, 50), (30, 30), (40, 40)

# Скорость игры
player_speed, ghost_speed, candy_speed = 5, 3, 4
TARGET_SCORE = 15

class GameSprite(pg.sprite.Sprite):
    def __init__(self, image, width, height, speed):
        super().__init__()
        self.image = pg.transform.scale(image, (width, height))
        self.rect = self.image.get_rect()
        self.speed = speed

class Player(GameSprite):
    def __init__(self, image, speed):
        super().__init__(image, *PLAYER_SIZE, speed)
        self.rect.centerx, self.rect.bottom = SCREEN_WIDTH // 2, SCREEN_HEIGHT
        self.size_increase = 5

    def update(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pg.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed

    def grow(self):
        new_width, new_height = self.rect.width + self.size_increase, self.rect.height + self.size_increase
        self.image = pg.transform.scale(images['player'], (new_width, new_height))
        self.rect.size = new_width, new_height
        self.rect.bottom = SCREEN_HEIGHT

class Entity(GameSprite):
    def __init__(self, image, width, height, speed):
        super().__init__(image, width, height, speed)
        self.rect.x, self.rect.y = randint(0, SCREEN_WIDTH - width), randint(-100, -height)

    def reset_position(self):
        self.rect.x = randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = randint(-100, -self.rect.height)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.reset_position()

def draw_text(text, font, color, x, y):
    screen.blit(font.render(text, True, color), (x, y))

def game():
    candies, ghosts = pg.sprite.Group(), pg.sprite.Group()
    player = Player(images['player'], player_speed)

    # Создание конфет и призраков
    for _ in range(5):
        candies.add(Entity(images['candy'], *CANDY_SIZE, candy_speed))
    for _ in range(3):
        ghosts.add(Entity(images['ghost'], *GHOST_SIZE, ghost_speed))

    # Игровые переменные
    score, run, clock = 0, True, pg.time.Clock()
    font = pg.font.SysFont(None, 48)
    game_over, win = False, False

    while run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_r and (game_over or win):
                    return True

        screen.blit(images['background'], (0, 0))

        if not game_over and not win:
            # Обновление спрайтов
            player.update()
            candies.update()
            ghosts.update()

            # Проверка на сбор конфет
            collected_candy = pg.sprite.spritecollideany(player, candies)
            if collected_candy:
                collected_candy.reset_position()
                score += 1
                player.grow()

            # Проверка на столкновение с призраком
            if pg.sprite.spritecollideany(player, ghosts):
                game_over = True

            # Проверка на победу
            if score >= TARGET_SCORE:
                win = True

            # Отображение элементов игры
            screen.blit(player.image, player.rect)
            candies.draw(screen)
            ghosts.draw(screen)
            draw_text(f'Score: {score}', font, WHITE, 10, 10)

        if game_over:
            draw_text("Game Over!", font, RED, SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2)
            draw_text("Press 'R' to Restart", font, WHITE, SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 + 50)

        elif win:
            draw_text("You Win! Press 'R' to Restart", font, ORANGE, SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2)
            draw_text("Press 'R' to Restart", font, WHITE, SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 + 50)


        pg.display.flip()
        clock.tick(60)

    return True

if __name__ == "__main__":
    while game():
        pass
    pg.quit()
