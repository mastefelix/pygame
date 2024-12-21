import pygame
import random

# Инициализация Pygame
pygame.init()
pygame.mixer.init()  # Инициализация микшера для работы со звуками

# Размеры окна
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Pixel Racers")

# Цвета
BLACK = (0, 0, 0)

# Скорость игры
SPEED = 5

# Шрифт для отображения счётчика времени и результатов
pygame.font.init()
font = pygame.font.SysFont(None, 36)

# Загрузка фоновой музыки и звуков
pygame.mixer.music.load('sounds/background_music.ogg')  # Загрузка фоновой музыки
pygame.mixer.music.play(-1)  # Воспроизведение музыки в цикле

collision_sound = pygame.mixer.Sound('sounds/collision.ogg')  # Звук столкновения
game_over_sound = pygame.mixer.Sound('sounds/game_over.ogg')  # Звук окончания игры


class Car:
    def __init__(self):
        self.width = 70
        self.height = 70
        self.x = WINDOW_WIDTH - 100  # Стартовая позиция ближе к правому краю
        self.y = WINDOW_HEIGHT // 2 - self.height // 2
        self.speed = SPEED
        self.image = pygame.image.load('images/car.png')
        self.image = pygame.transform.scale(self.image, (self.width, self.height))

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

    def move(self, keys):
        if keys[pygame.K_UP] and self.y > 0:
            self.y -= self.speed
        if keys[pygame.K_DOWN] and self.y < WINDOW_HEIGHT - self.height:
            self.y += self.speed


class Obstacle:
    def __init__(self):
        self.width = 50
        self.height = 50
        self.x = -self.width
        self.y = random.randint(0, WINDOW_HEIGHT - self.height)

        self.image = pygame.image.load('images/cone.png')
        self.image = pygame.transform.scale(self.image, (self.width, self.height))

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

    def move(self):
        self.x += SPEED

    def off_screen(self):
        return self.x > WINDOW_WIDTH


class Game:
    def __init__(self):
        self.running = True
        self.clock = pygame.time.Clock()
        self.car = Car()
        self.obstacles = []
        self.start_time = pygame.time.get_ticks()  # Запоминаем время начала игры
        self.elapsed_time = 0  # Время, проведённое в игре до момента проигрыша
        self.background = pygame.image.load('images/background.jpg')  # Загрузка фоновой картинки
        self.background = pygame.transform.scale(self.background, (WINDOW_WIDTH, WINDOW_HEIGHT))

    def create_obstacle(self):
        if random.randint(1, 20) == 1:
            self.obstacles.append(Obstacle())

    def move_obstacles(self):
        for obstacle in self.obstacles:
            obstacle.move()

        # Удаляем препятствия, которые вышли за экран
        self.obstacles = [obstacle for obstacle in self.obstacles if not obstacle.off_screen()]

    def check_collision(self):
        for obstacle in self.obstacles:
            if self.car.y < obstacle.y + obstacle.height and self.car.y + self.car.height > obstacle.y:
                if self.car.x < obstacle.x + obstacle.width and self.car.x + self.car.width > obstacle.x:
                    self.elapsed_time = (pygame.time.get_ticks() - self.start_time) // 1000  # Записываем время
                    pygame.mixer.Sound.play(collision_sound)  # Воспроизведение звука столкновения
                    self.running = False  # Конец игры при столкновении

    def draw_elements(self):
        # Отрисовываем фон
        screen.blit(self.background, (0, 0))
        self.car.draw()
        for obstacle in self.obstacles:
            obstacle.draw()

        # Отображаем время, проведённое в игре
        elapsed_time = (pygame.time.get_ticks() - self.start_time) // 1000  # Время в секундах
        time_text = font.render(f"Время: {elapsed_time} с", True, BLACK)
        screen.blit(time_text, (10, 10))  # Рисуем текст в левом верхнем углу

    def game_over_screen(self):
        screen.fill((255, 255, 255))  # Белый фон для экрана конца игры
        result_text = font.render(f"Game Over! Время: {self.elapsed_time} с", True, BLACK)
        screen.blit(result_text, (WINDOW_WIDTH // 2 - result_text.get_width() // 2, WINDOW_HEIGHT // 3))

        restart_text = font.render("Нажми R для перезапуска или Q для выхода", True, BLACK)
        screen.blit(restart_text, (WINDOW_WIDTH // 2 - restart_text.get_width() // 2, WINDOW_HEIGHT // 2))

        pygame.mixer.Sound.play(game_over_sound)  # Воспроизведение звука окончания игры

        pygame.display.flip()

        # Ожидание действий игрока
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return False
                keys = pygame.key.get_pressed()
                if keys[pygame.K_r]:  # Перезапуск игры
                    return True
                if keys[pygame.K_q]:  # Выход из игры
                    pygame.quit()
                    return False

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            keys = pygame.key.get_pressed()
            self.car.move(keys)
            self.create_obstacle()
            self.move_obstacles()
            self.check_collision()
            self.draw_elements()

            pygame.display.flip()
            self.clock.tick(60)

        # Когда игра заканчивается, показываем экран результатов
        if not self.running:
            if self.game_over_screen():
                self.__init__()  # Перезапуск игры
                game_over_sound.stop()
                self.run()


# Запуск игры
if __name__ == "__main__":
    game = Game()
    game.run()
