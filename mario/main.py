import pygame as pg
import level
import player
import camera
import os
from random import randint
pg.init()

# Константы для настройки окна
WIN_WIDTH = 800
WIN_HEIGHT = 640
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
FPS = 60  # Частота кадров

screen = pg.display.set_mode(DISPLAY)
pg.display.set_caption("Super Mario")

def game(level_number = 1):
    """Основная игровая функция."""
    path = f'levels/{level_number}.txt'
    # Загрузка фонового изображения
    bg_img = f'images/bg{level_number}.gif'
    bg = pg.transform.scale(pg.image.load(bg_img), (1300, 960))
    level_1 = level.Level(path)
    # Загрузка музыки
    pg.mixer.init()
    pg.mixer.music.load("sounds/super-mario-saundtrek.mp3")
    pg.mixer.music.play(-1)  # Зацикливание музыки
    fail = pg.mixer.Sound('sounds/game-over.mp3')
    win = pg.mixer.Sound('sounds/win.mp3')

    # Таймер для управления кадрами
    clock = pg.time.Clock()
    entities = pg.sprite.Group()  # Все объекты
    # level_1 = level.Level()  # Уровень
    total_level_width = (len(level_1.load()[0]) - 1) * level.platform.PLATFORM_WIDTH
    total_level_height = (len(level_1.load())) * level.platform.PLATFORM_HEIGHT
    main_camera = camera.Camera(total_level_width, total_level_height)
    hero = player.Player(55, 55)
    entities.add(hero)
    platforms = level_1.getPlatform()  # Платформы, в которые упираемся или врезаемся
    for platform in platforms:
        entities.add(platform)



    animatedEntities = pg.sprite.Group()
    for _ in range(3):
        tp = level.platform.BlockTeleport(randint(50, 1200), randint(50, 1200))
        entities.add(tp)
        platforms.append(tp)
        animatedEntities.add(tp)

    # Все передвигающиеся объекты
    monsters = pg.sprite.Group()
    for _ in range(5):
        mn = player.monsters.Monster(randint(50, 1200), randint(50, 1200), randint(1, 5),
                                     randint(1, 5), randint(100, 200), randint(100, 200))
        entities.add(mn)
        platforms.append(mn)
        monsters.add(mn)

    level_1.getPrincess(entities, animatedEntities, platforms)

    # Основной игровой цикл
    run = True
    while run:
        for event in pg.event.get():
            if event.type == pg.QUIT:  # Выход из игры
                pg.mixer.music.stop()  # Остановка музыки при выходе из игры
                run = False
            hero.move(event)
        if not hero.game_over:
            # Рисуем фон
            screen.blit(bg, main_camera.state.topleft)
            hero.update(platforms)
            main_camera.update(hero)
            for entity in entities:
                screen.blit(entity.image, main_camera.apply(entity))
            animatedEntities.update()
            monsters.update(platforms)  # передвигаем всех монстров
        else:
            pg.mixer.music.stop()
            fail.play()
            font = pg.font.SysFont('fonts/supermario286rusbylyajka.otf', 100)  # Используем шрифт
            text = font.render("Игра окончена!", True, (255, 0, 0))  # Красный цвет текста
            text_rect = text.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2))
            screen.blit(text, text_rect)
            pg.display.update()
            pg.time.wait(5000)  # Пауза на 5 секунд перед завершением
            run = False
            pg.mixer.music.stop()
        if hero.winner:
            hero.winner = False
            level_number += 1
            path = f'levels/{level_number}.txt'
            if os.path.isfile(path):
                pg.mixer.music.stop()
                win.play()
                font = pg.font.SysFont('fonts/supermario286rusbylyajka.otf', 100)  # Используем шрифт
                text = font.render("Уровень пройден!", True, (0, 255, 0))  # Красный цвет текста
                text_rect = text.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2))
                screen.blit(text, text_rect)
                pg.display.update()
                pg.time.wait(5000)
                game(level_number)
                return
            else:
                pg.mixer.music.stop()
                win.play()
                font = pg.font.SysFont('fonts/supermario286rusbylyajka.otf', 100)  # Используем шрифт
                text = font.render("Все уровни пройдены!", True, (0, 255, 0))  # Красный цвет текста
                text_rect = text.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2))
                screen.blit(text, text_rect)
                pg.display.update()
                pg.time.wait(5000)  # Пауза на 5 секунд перед завершением
                pg.mixer.music.stop()
                run = False


        # Обновляем экран
        pg.display.update()
        clock.tick(FPS)


if __name__ == "__main__":
    from menu import main_menu
    main_menu()
    pg.quit()
