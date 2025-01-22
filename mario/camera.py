import pygame as pg

class Camera:
    def __init__(self, width, height, win_width=800, win_height=640, scale=1):
        """
        Инициализация камеры.
        width: Ширина уровня
        height: Высота уровня
        win_width: Ширина окна
        win_height: Высота окна
        Коэффициент масштабирования
        """
        self.camera_func = self.camera_configure
        self.state = pg.Rect(0, 0, width, height)
        self.win_width = win_width
        self.win_height = win_height
        self.scale = scale

    def apply(self, target):
        """
        Применяет смещение камеры к объекту.
        target: Объект, к которому применяется камера
        return: Смещенный прямоугольник объекта
        """
        return target.rect.move(self.state.topleft).inflate(
            -self.state.width * (1 - self.scale), -self.state.height * (1 - self.scale)
        )

    def update(self, target):
        """
        Обновляет положение камеры на основе цели.
        target: Объект, за которым следит камера
        """
        self.state = self.camera_func(self.state, target.rect, self.win_width, self.win_height)

    @staticmethod
    def camera_configure(camera, target_rect, win_width, win_height):
        """
        Настраивает положение камеры.
        camera: Прямоугольник камеры
        target_rect: Прямоугольник цели
        win_width: Ширина окна
        win_height: Высота окна
        return: Новое положение камеры
        """
        left = max(-(camera.width - win_width), min(0, -target_rect.centerx + win_width / 2))
        top = max(-(camera.height - win_height), min(0, -target_rect.centery + win_height / 2))
        return pg.Rect(left, top, camera.width, camera.height)


