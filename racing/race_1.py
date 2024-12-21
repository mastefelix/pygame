import pygame
import random

# Инициализация Pygame
pygame.init()

# Размеры окна
window_size = (800, 600)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Pixel Racers")

# Цвета
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Загрузка машины
car_width = 40
car_height = 70
player_car = pygame.image.load('images/car.png')
player_car = pygame.transform.scale(player_car, (car_width, car_height))

# Начальные параметры машины
car_x, car_y = window_size[0] - car_width - 50, window_size[1] // 2 - car_height // 2
speed = 5

# Препятствия
obstacle_width = 50
obstacle_height = 50
obstacle_color = (255, 0, 0)
obstacles = []


def draw_car(x, y):
    screen.blit(player_car, (x, y))


def create_obstacle():
    obstacle_x =  - obstacle_width
    obstacle_y = random.randint(0, window_size[0]-obstacle_height)
    obstacles.append([obstacle_x, obstacle_y])


def move_obstacles():
    for obstacle in obstacles:
        obstacle[0] += speed
        if obstacle[0] > window_size[0]:
            obstacles.remove(obstacle)


def draw_obstacles():
    for obstacle in obstacles:
        pygame.draw.rect(screen, obstacle_color, [obstacle[0], obstacle[1], obstacle_width, obstacle_height])


# Основной цикл игры
running = True
clock = pygame.time.Clock()

while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # Управление машиной
    if keys[pygame.K_UP] and car_y > 0:
        car_y -= speed
    if keys[pygame.K_DOWN] and car_y < window_size[1] - car_height:
        car_y += speed

    draw_car(car_x, car_y)

    # Создание и перемещение препятствий
    if random.randint(1, 20) == 1:
        create_obstacle()

    move_obstacles()
    draw_obstacles()

    # Проверка на столкновение
    for obstacle in obstacles:
        if car_y < obstacle[1] + obstacle_height and car_y + car_height > obstacle[1]:
            if car_x < obstacle[0] + obstacle_width and car_x + car_width > obstacle[0]:
                running = False  # Конец игры при столкновении

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
