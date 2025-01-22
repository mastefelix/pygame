import pygame as pg
import level
import player
pg.init()

# Константы для настройки окна
WIN_WIDTH = 800
WIN_HEIGHT = 640
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
FPS = 60  # Частота кадров

screen = pg.display.set_mode(DISPLAY)
pg.display.set_caption("Super Mario")

def game():
    """Основная игровая функция."""
    bg_img = 'images/bg1.gif' # Загрузка фонового изображения
    bg = pg.transform.scale(pg.image.load(bg_img), (1300, 960))
    # Загрузка музыки
    pg.mixer.init()
    pg.mixer.music.load("sounds/super-mario-saundtrek.mp3")
    pg.mixer.music.play(-1)  # Зацикливание музыки
    # Таймер для управления кадрами
    clock = pg.time.Clock()
    entities = pg.sprite.Group()  # Все объекты
    level_1 = level.Level()  # Уровень
    platforms = level_1.getPlatform()
    for platform in platforms:
        entities.add(platform)
    hero = player.Player(55, 55)
    entities.draw(hero)
    # Основной игровой цикл
    run = True
    while run:
        for event in pg.event.get():
            if event.type == pg.QUIT:  # Выход из игры
                pg.mixer.music.stop()  # Остановка музыки при выходе из игры
                run = False
        screen.blit(bg, (0, 0))
        hero.update(platforms)
        entities.draw(screen)
        # Обновляем экран
        pg.display.update()
        clock.tick(FPS)
    pg.quit()
if __name__ == "__main__":
    game()



 # if hero.winner:
        #     pg.mixer.music.stop()
        #     win.play()
        #     font = pg.font.SysFont('fonts/supermario286rusbylyajka.otf', 100)  # Используем шрифт
        #     text = font.render("Win!", True, (0, 255, 0))  # Красный цвет текста
        #     text_rect = text.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2))
        #     screen.blit(text, text_rect)
        #     pg.display.update()
        #     pg.time.wait(5000)  # Пауза на 5 секунд перед завершением
        #     run = False
        #     pg.mixer.music.stop()
