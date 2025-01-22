import pygame as pg
import pyganim

PLATFORM_WIDTH = 32  # Ширина прямоугольника
PLATFORM_HEIGHT = 32  # Высота прямоугольника

ANIMATION_BLOCK_TELEPORT = ['images/portal1.png', 'images/portal2.png']
ANIMATION_PRINCESS = ['images/princess_l.png', 'images/princess_r.png']


class Platform(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image = pg.image.load('images/platform.png')
        self.rect = pg.Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)


class BlockDie(Platform):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = pg.transform.scale(pg.image.load('images/dieBlock.png'), (PLATFORM_WIDTH, PLATFORM_HEIGHT))


class BlockTeleport(Platform):
    def __init__(self, x, y):
        super().__init__(x, y)
        boltAnim = list()
        for anim in ANIMATION_BLOCK_TELEPORT:
            boltAnim.append((anim, 1))
        self.boltAnim = pyganim.PygAnimation(boltAnim)
        self.boltAnim.play()

    def update(self):
        self.image.fill(pg.Color('#7686FF'))
        self.boltAnim.blit(self.image, (0, 0))


class Princess(Platform):
    def __init__(self, x, y):
        super().__init__(x, y)
        boltAnim = list()
        for anim in ANIMATION_PRINCESS:
            boltAnim.append((anim, 600))
        self.boltAnim = pyganim.PygAnimation(boltAnim)
        self.boltAnim.play()

    def update(self):
        self.image.fill(pg.Color('#7686FF'))
        self.boltAnim.blit(self.image, (0, 0))


