import platform

FILE_DIR = 'levels/1.txt'  # Путь к файлу уровня


class Level:
    pathLevel: str  # Получение информации о пути к файлу в виде строки

    def __init__(self, path=FILE_DIR):  # Создание конструктора класса
        self.pathLevel = path

    def load(self):  # Загрузка файла уровня
        with open(self.pathLevel) as file:
            level = file.readlines()
        return level

    def getPlatform(self):  # Метод для возвращения объектов
        platforms = []
        x = y = 0  # Координаты
        for row in self.load():  # Вся строка
            for col in row:  # Каждый символ
                if col == '-':  # Если найдем -
                    pf = platform.Platform(x, y)
                    platforms.append(pf)
                elif col == '*':
                    block_die = platform.BlockDie(x, y)
                    platforms.append(block_die)
                elif col == '+':
                    block_teleport = platform.BlockTeleport(x, y)
                    platforms.append(block_teleport)
                    block_teleport.update()
                x += platform.PLATFORM_WIDTH
            y += platform.PLATFORM_HEIGHT
            x = 0
        return platforms

    def getPrincess(self, entities, animatedEntities, platforms):
        x = y = 0
        for row in self.load():
            for col in row:
                if col == 'P':
                    pr = platform.Princess(x, y)
                    entities.add(pr)
                    platforms.append(pr)
                    animatedEntities.add(pr)
                x += platform.PLATFORM_WIDTH
            y += platform.PLATFORM_HEIGHT
            x = 0

