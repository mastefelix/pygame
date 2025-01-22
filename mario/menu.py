import pygame as pg
from main import *

# Путь к шрифту
FONT_PATH = 'fonts/supermario286rusbylyajka.otf'
path = 'levels/1.txt'
# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

def draw_text(surface, text, size, x, y, color=WHITE):
    """Рисует текст на экране."""
    font = pg.font.Font(FONT_PATH, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    surface.blit(text_surface, text_rect)

def main_menu():
    """Функция отображения стартового меню."""
    # Таймер для управления кадрами
    clock = pg.time.Clock()
    # Загрузка и масштабирование фонового изображения
    bg = pg.transform.scale(pg.image.load('images/bg_mario__9_darken.jpg'), DISPLAY)
    # Шрифт
    font_size = 50
    while True:
        if not pg.mixer.music.get_busy():
            pg.mixer.init()
            pg.mixer.music.load("sounds/menu.mp3")
            pg.mixer.music.play(-1)  # Зацикливание музыки
        # Рисуем кнопки
        play_rect = pg.Rect(WIN_WIDTH // 2 - 150, WIN_HEIGHT // 2 - 40, 300, 80)
        quit_rect = pg.Rect(WIN_WIDTH // 2 - 150, WIN_HEIGHT // 2 + 100, 300, 80)
        for event in pg.event.get():
            if event.type == pg.QUIT:  # Закрытие окна
                exit()
            # Обработка событий мыши
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:  # Левая кнопка мыши
                mouse_pos = pg.mouse.get_pos()
                if play_rect.collidepoint(mouse_pos):  # Кнопка "Играть"
                    game()  # Переход к игре
                if quit_rect.collidepoint(mouse_pos):  # Кнопка "Выход"
                    exit()
        # Отображаем фоновое изображение
        screen.blit(bg, (0, 0))
        # Рисуем текст
        draw_text(screen, "Super Mario", 70, WIN_WIDTH // 2, WIN_HEIGHT // 4, RED)
        draw_text(screen, "Играть", font_size, WIN_WIDTH // 2, WIN_HEIGHT // 2)
        draw_text(screen, "Выход", font_size, WIN_WIDTH // 2, WIN_HEIGHT // 2 + 140)
        # Рисуем рамки для кнопок
        pg.draw.rect(screen, WHITE, play_rect, 3)
        pg.draw.rect(screen, WHITE, quit_rect, 3)
        # Обновляем экран
        pg.display.update()
        clock.tick(FPS)


