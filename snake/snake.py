import pygame as pg
import random

# Инициализация Pygame
pg.init()

# Настройки окна игры
WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20
SCREEN = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Змейка")

# Цвета
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Шрифт
FONT = pg.font.SysFont("comicsansms", 35)

# Класс для змейки
class Snake:
    def __init__(self):
        self.body = [(100, 100), (90, 100), (80, 100)]  # начальная длина змейки
        self.direction = pg.K_RIGHT  # направление движения
        self.grow = False  # флаг роста змейки

    def move(self):
        head_x, head_y = self.body[0]
        if self.direction == pg.K_RIGHT:
            head_x += CELL_SIZE
        elif self.direction == pg.K_LEFT:
            head_x -= CELL_SIZE
        elif self.direction == pg.K_UP:
            head_y -= CELL_SIZE
        elif self.direction == pg.K_DOWN:
            head_y += CELL_SIZE

        new_head = (head_x, head_y)
        self.body.insert(0, new_head)

        if not self.grow:
            self.body.pop()
        else:
            self.grow = False

    def change_direction(self, new_direction):
        # Не позволяем змейке двигаться в противоположную сторону
        opposite_directions = {
            pg.K_UP: pg.K_DOWN,
            pg.K_DOWN: pg.K_UP,
            pg.K_LEFT: pg.K_RIGHT,
            pg.K_RIGHT: pg.K_LEFT
        }
        if new_direction != opposite_directions.get(self.direction):
            self.direction = new_direction

    def check_collision(self):
        # Проверка столкновения с границами экрана
        head_x, head_y = self.body[0]
        if head_x < 0 or head_x >= WIDTH or head_y < 0 or head_y >= HEIGHT:
            return True

        # Проверка столкновения с телом змейки
        if (head_x, head_y) in self.body[1:]:
            return True

        return False

    def grow_snake(self):
        self.grow = True

    def draw(self):
        for segment in self.body:
            pg.draw.rect(SCREEN, GREEN, (*segment, CELL_SIZE, CELL_SIZE))

# Класс для еды
class Food:
    def __init__(self):
        self.position = self.random_position()

    def random_position(self):
        return (
            random.randint(0, (WIDTH // CELL_SIZE) - 1) * CELL_SIZE,
            random.randint(0, (HEIGHT // CELL_SIZE) - 1) * CELL_SIZE
        )

    def draw(self):
        pg.draw.rect(SCREEN, RED, (*self.position, CELL_SIZE, CELL_SIZE))

# Функция для отображения текста
def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    SCREEN.blit(text_surface, (x, y))

# Главная функция игры
def game_loop():
    clock = pg.time.Clock()
    snake = Snake()
    food = Food()
    score = 0  # Начальное количество очков
    run = True

    while run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            elif event.type == pg.KEYDOWN:
                snake.change_direction(event.key)

        snake.move()

        # Проверка на поедание еды
        if snake.body[0] == food.position:
            snake.grow_snake()
            food.position = food.random_position()
            score += 1  # Увеличение счета на 10 за каждую еду

        # Проверка на столкновение
        if snake.check_collision():
            # Отображаем сообщение о проигрыше и счет
            draw_text("Game Over", FONT, RED, WIDTH // 2 - 100, HEIGHT // 2 - 50)
            draw_text(f"Score: {score}", FONT, WHITE, WIDTH // 2 - 80, HEIGHT // 2 + 10)
            pg.display.update()
            pg.time.delay(2000)  # Пауза в 2 секунды перед выходом
            run = False

        SCREEN.fill(BLACK)
        snake.draw()
        food.draw()

        # Отображаем текущий счет
        draw_text(f"Score: {score}", FONT, WHITE, 10, 10)

        pg.display.update()

        clock.tick(10)  # Ограничение FPS

    pg.quit()

# Запуск игры
if __name__ == "__main__":
    game_loop()
