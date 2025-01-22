import level
import player
import platform
import camera

class LevelManager:
    def __init__(self):
        self.current_level_index = 0
        self.levels = ['levels/1.txt', 'levels/2.txt']  # Добавьте пути к вашим уровням
        self.level_objects = []

    def load_current_level(self):
        """
        Загружает текущий уровень и возвращает необходимые объекты.
        """
        path = self.levels[self.current_level_index]
        current_level = level.Level(path)
        platforms = current_level.getPlatform()
        entities = player.pg.sprite.Group()
        animated_entities = player.pg.sprite.Group()

        # Создаем основные игровые объекты
        hero = player.Player(55, 55)
        entities.add(hero)

        # Добавляем все платформы и объекты уровня
        for platform_obj in platforms:
            entities.add(platform_obj)

        current_level.getPrincess(entities, animated_entities, platforms)

        total_level_width = (len(current_level.load()[0]) - 1) * platform.PLATFORM_WIDTH
        total_level_height = (len(current_level.load())) * platform.PLATFORM_HEIGHT
        game_camera = camera.Camera(total_level_width, total_level_height)

        return hero, platforms, entities, animated_entities, game_camera

    def next_level(self):
        """
        Переходит к следующему уровню, если он существует.
        """
        self.current_level_index += 1
        if self.current_level_index >= len(self.levels):
            print("Игра пройдена!")
            return None
        return self.load_current_level()

    def reset(self):
        """
        Сброс уровня к первому.
        """
        self.current_level_index = 0
        return self.load_current_level()
