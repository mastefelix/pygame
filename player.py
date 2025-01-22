import pygame as pg
import pyganim
import platform
import monsters
from random import randint

MOVE_SPEED = 7
PLAYER_WIDTH = 22
PLAYER_HEIGHT = 32
COLOR = '#000000'
JUMP_POWER = 15
GRAVITY = 0.35

ANIMATION_DELAY = 2
ANIMATION_RIGHT = ['images/r1.png',
                   'images/r2.png',
                   'images/r3.png',
                   'images/r4.png',
                   'images/r5.png']
ANIMATION_LEFT = ['images/l1.png',
                  'images/l2.png',
                  'images/l3.png',
                  'images/l4.png',
                  'images/l5.png']
ANIMATION_JUMP_RIGHT = [('images/jr.png', ANIMATION_DELAY)]
ANIMATION_JUMP_LEFT = [('images/jl.png', ANIMATION_DELAY)]
ANIMATION_JUMP = [('images/j.png', ANIMATION_DELAY)]
ANIMATION_STAY = [('images/0.png', ANIMATION_DELAY)]


class Player(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.game_over = False
        self.speed_x = 0  # Скорость по X
        self.speed_y = 0  # Скорость по Y
        self.image = pg.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
        self.image.fill(pg.Color(COLOR))
        self.rect = pg.Rect(x, y, PLAYER_WIDTH, PLAYER_HEIGHT)
        self.left = self.right = self.up = self.onGround = False
        self.image.set_colorkey(pg.Color(COLOR))
        self.winner = False

        bolt_anim = list()
        for anim in ANIMATION_RIGHT:
            bolt_anim.append((anim, ANIMATION_DELAY))
        self.boltAnimRight = pyganim.PygAnimation(bolt_anim)
        self.boltAnimRight.play()

        bolt_anim.clear()
        for anim in ANIMATION_LEFT:
            bolt_anim.append((anim, ANIMATION_DELAY))
        self.boltAnimLeft = pyganim.PygAnimation(bolt_anim)
        self.boltAnimLeft.play()
        bolt_anim.clear()

        self.boltAnimStay = pyganim.PygAnimation(ANIMATION_STAY)
        self.boltAnimStay.play()
        self.boltAnimStay.blit(self.image, (0, 0))

        self.boltAnimJumpLeft = pyganim.PygAnimation(ANIMATION_JUMP_LEFT)
        self.boltAnimJumpLeft.play()

        self.boltAnimJumpRight = pyganim.PygAnimation(ANIMATION_JUMP_RIGHT)
        self.boltAnimJumpRight.play()

        self.boltAnimJump = pyganim.PygAnimation(ANIMATION_JUMP)
        self.boltAnimJump.play()

    def update(self, platforms):
        self.image.fill(pg.Color(COLOR))
        # Обновление скорости
        if self.left:
            self.speed_x = -MOVE_SPEED
            if self.up:
                self.boltAnimJumpLeft.blit(self.image, (0, 0))
            else:
                self.boltAnimLeft.blit(self.image, (0, 0))
        if self.right:
            self.speed_x = MOVE_SPEED
            if self.up:
                self.boltAnimJumpRight.blit(self.image, (0, 0))
            else:
                self.boltAnimRight.blit(self.image, (0, 0))
        if not (self.left or self.right):
            self.speed_x = 0
            self.boltAnimStay.blit(self.image, (0, 0))
        if self.up and self.onGround:
            self.speed_y = -JUMP_POWER
        if self.up:
            self.boltAnimJump.blit(self.image, (0, 0))


        if not self.onGround:
            self.speed_y += GRAVITY

        # Сброс флага
        self.onGround = False
        # Обновление позиции
        self.rect.y += self.speed_y
        self.collide(0, self.speed_y, platforms)
        self.rect.x += self.speed_x
        self.collide(self.speed_x, 0, platforms)

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def collide(self, player_x, player_y, platforms):
        for p in platforms:
            if pg.sprite.collide_rect(self, p):
                if isinstance(p, platform.BlockDie) or isinstance(p, monsters.Monster):
                    self.die()
                if isinstance(p, platform.BlockTeleport):
                    self.teleporting(randint(50, 700), randint(50, 550))
                if isinstance(p, platform.Princess):
                    self.winner = True
                if player_x > 0:  # Движение вправо
                    self.rect.right = p.rect.left
                if player_x < 0:  # Движение влево
                    self.rect.left = p.rect.right
                if player_y > 0:  # Движение вниз
                    self.rect.bottom = p.rect.top
                    self.onGround = True
                    self.speed_y = 0
                if player_y < 0:  # Движение вверх
                    self.rect.top = p.rect.bottom
                    self.speed_y = 0

    def move(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT:
                self.left = True
            if event.key == pg.K_RIGHT:
                self.right = True
            if event.key == pg.K_UP:
                self.up = True

        elif event.type == pg.KEYUP:
            if event.key == pg.K_LEFT:
                self.left = False
            if event.key == pg.K_RIGHT:
                self.right = False
            if event.key == pg.K_UP:
                self.up = False

    def die(self):
        pg.time.wait(500)
        self.game_over = True

    def teleporting(self, goX, goY):
        self.rect.x = goX
        self.rect.y = goY

