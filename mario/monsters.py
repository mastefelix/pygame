import pygame as pg
import pyganim

MONSTER_WIDTH = 32
MONSTER_HEIGHT = 32
MONSTER_COLOR = '#2110FF'
ANIMATION_DELAY = 1  # Задержка анимации в миллисекундах
ANIMATION_MONSTER = ['images/fire1.png', 'images/fire2.png']


class Monster(pg.sprite.Sprite):
    def __init__(self, x, y, speed_x, speed_y, x_range, y_range, width=MONSTER_WIDTH, height=MONSTER_HEIGHT):
        super().__init__()
        self.startX = x  # начальная позиция по X
        self.startY = y  # начальная позиция по Y
        self.speed_x = speed_x  # скорость по X
        self.speed_y = speed_y  # скорость по Y
        self.x_range = x_range  # максимальное смещение по X
        self.y_range = y_range  # максимальное смещение по Y

        # Создание изображения монстра
        self.image = pg.Surface((width, height))  # width: ширина монстра, height: высота монстра
        self.image.fill(pg.Color(MONSTER_COLOR))
        self.rect = pg.Rect(x, y, MONSTER_WIDTH, MONSTER_HEIGHT)
        self.image.set_colorkey(pg.Color(MONSTER_COLOR))

        # Анимация монстра
        self.boltAnim = pyganim.PygAnimation([(anim, ANIMATION_DELAY) for anim in ANIMATION_MONSTER])
        self.boltAnim.play()

    def update(self, platforms):
        # Обновление анимации
        self.image.fill(pg.Color(MONSTER_COLOR))  # Резервный цвет (если нет анимации)
        self.boltAnim.blit(self.image, (0, 0))

        # Перемещение монстра
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        # Проверка столкновений
        self.collide(platforms)

        # Проверка границ перемещения
        if abs(self.startX - self.rect.x) < self.x_range:
            self.speed_x *= -1
        if abs(self.startY - self.rect.y) < self.y_range:
            self.speed_y *= -1

    def collide(self, platforms):
        for p in platforms:
            if pg.sprite.collide_rect(self, p):
                self.speed_x *= -1
                self.speed_y *= -1




