import pygame as pg
from random import randint

# Инициализация Pygame
pg.init()

# Параметры экрана
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption("GameSprite Adventure")

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
ORANGE = (255, 165, 0)
RED = (255, 0, 0)

# Ссылки на изображения
pumpkin_image = 'images/pumpkin.png'
candy_image = 'images/candy.png'
ghost_image = 'images/ghost.png'

# Размеры объектов
player_width, player_height = 50, 50
candy_width, candy_height = 30, 30
ghost_width, ghost_height = 40, 40

# Скорость игры
player_speed = 5
ghost_speed = 3
candy_speed = 4

# Количество конфет для победы
TARGET_SCORE = 30

# Общий класс
class GameSprite(pg.sprite.Sprite):
    def __init__(self, image, width, height, speed):
        super().__init__()
        self.image = pg.transform.scale(pg.image.load(image), (width, height))
        self.rect = self.image.get_rect()
        self.speed = speed

# Класс игрока
class Player(GameSprite):
    def __init__(self, image, width, height, speed):
        super().__init__(image, width, height, speed)
        self.rect.x = SCREEN_WIDTH // 2
        self.rect.y = SCREEN_HEIGHT - height

    def update(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pg.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed


# Класс падающих объектов
class Entity(GameSprite):
    def __init__(self, image, width, height, speed):
        super().__init__(image, width, height, speed)
        self.rect.x = randint(0, SCREEN_WIDTH - width)
        self.rect.y = randint(-100, -height)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.x = randint(0, SCREEN_WIDTH - self.rect.width)
            self.rect.y = randint(-100, -self.rect.height)


# Функция отображения текста
def draw_text(text, font, color, x, y):
    render = font.render(text, True, color)
    screen.blit(render, (x, y))


# Основная функция игры
def game():
    # Создание групп спрайтов
    candies = pg.sprite.Group()
    ghosts = pg.sprite.Group()

    # Создание игрока
    player = Player(pumpkin_image, player_width, player_height, player_speed)

    # Создание конфет
    for _ in range(5):
        candies.add(Entity(candy_image, candy_width, candy_height, candy_speed))

    # Создание призраков
    for _ in range(3):
        ghosts.add(Entity(ghost_image, ghost_width, ghost_height, ghost_speed))

    # Игровые переменные
    score = 0
    run = True
    clock = pg.time.Clock()
    font = pg.font.SysFont(None, 36)
    game_over = False
    win = False

    while run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False

        if not game_over and not win:
            # Обновление спрайтов
            player.update()
            candies.update()
            ghosts.update()
            screen.fill(BLACK)
            screen.blit(player.image, player.rect)
            candies.draw(screen)
            ghosts.draw(screen)

            # Проверка на сбор конфет
            collected_candy = pg.sprite.spritecollideany(player, candies)
            if collected_candy:
                collected_candy.kill()
                score += 1
                # Создание новой конфеты
                new_candy = Entity(candy_image, candy_width, candy_height, candy_speed)
                candies.add(new_candy)

            # Проверка на столкновение с призраком
            if pg.sprite.spritecollideany(player, ghosts):
                game_over = True  # Игра заканчивается

            # Проверка на победу
            if score >= TARGET_SCORE:
                win = True  # Игрок выиграл

        if game_over:
            draw_text("Game Over!", font, RED, SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2)
        elif win:
            draw_text("You Win!", font, ORANGE, SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2)

        draw_text(f'Score: {score}', font, WHITE, 10, 10)

        pg.display.flip()

        # Ограничение FPS
        clock.tick(60)

    pg.quit()


if __name__ == "__main__":
    game()
