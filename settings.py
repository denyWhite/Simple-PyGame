class Settings():
    def __init__(self, screen):
        self.framerate = 50  # Framerate
        self.test = True  # Тестовый режим

        self.screen_width = screen.get_rect().width
        self.screen_height = screen.get_rect().height

        self.capthion = "My game" # Заголовок экрана
        self.mouse_visible = False  # Видимость мышки
        self.bg_color = (16,16,16)  # Цвет фона
        self.color = (230, 230, 230)  # Цвет текста
        self.navy_blue_color = (0, 0, 128)  # Темно-синий

        self.max_lifes = 3  # Количество жизней
        self.score_for_alien = 3  # Очков за убитого чужого
        self.minus_if_miss = True  # Убавлять одно очко, если промах

        self.status_height = self.screen_width // 30

        # Параметры корабля
        self.ship_speed = 150 # За сколько тиков корабль переместиться на всю ширину экрана
        self.ship_ratio = 15 # Сколько кораблей поместиться в ширину экрана
        self.ship_speed_factor = self.screen_width / self.ship_speed
        self.ship_width = self.screen_width // self.ship_ratio
        self.ship_height = int(self.ship_width * 1.4825)

        # Параметры пули
        self.bullet_speed = 50  # За сколько тиков пуля достигнет ширину экрана
        self.bullet_color = (230, 230, 230)  # Цвет пули
        self.bullet_max_count = 1  # Максимальное колличество пуль на экране
        self.bullet_width_ratio = 300  # Сколько пуль уместиться в ширину экрана по ширине
        self.bullet_height_ratio = 100  # Сколько пуль уместиться в ширину экрана по длинне
        self.bullet_destroy = True  # Уничтожать ли пулю при столкновении или она летит дальше
        self.bullet_speed_factor = self.screen_width / self.bullet_speed
        self.bullet_width = self.screen_width // self.bullet_width_ratio
        self.bullet_height = self.screen_width // self.bullet_height_ratio


        # Параметры пришельца
        self.alien_ratio = 16  # Сколько пришельцев посместиться в ширину экрана
        self.alien_space_ratio = 90  # Расстояние между пришельцами по высоте
        self.alien_speed = 1500 # За сколько тиков чужой пролетит весь экран
        self.fleet_drop = 100  # За сколько тиков флот опуститься на ширину экрана

        self.level = 1
        self.levels = { 1 : [10, 7, 9, 8 ],
                              2 : [12, 9, 12, 9],
                              3 : [13, 11, 13, 11],
                              4 : [13, 12, 13, 12, 13],
                              5 : [14, 14, 14, 14, 14] }
        self.level_count = len(self.levels)

        self.fleet_drop_speed = self.screen_width // self.fleet_drop
        self.fleet_direction = 1
        self.alien_speed_factor = self.screen_width / self.alien_speed
        self.alien_space = self.screen_width // self.alien_space_ratio
        self.alien_width = self.screen_width // self.alien_ratio
        self.alien_height = int(self.alien_width * 0.705)
        if self.test:
            self.bullet_destroy = False
            self.bullet_width = 300
            self.alien_speed_factor = 30
            self.alien_level_count = 1

    def next_lvl(self):
        self.level += 1
        if self.level > self.level_count:
            return True
        else:
            self.alien_speed -= 200
            self.alien_speed_factor = self.screen_width / self.alien_speed
            self.fleet_drop -= 15
            self.fleet_drop_speed = self.screen_width // self.fleet_drop
            #self.bullet_max_count += 1
            self.ship_speed -= 15
            self.ship_speed_factor = self.screen_width / self.ship_speed
            self.bullet_speed += 10
            self.bullet_speed_factor = self.screen_width / self.bullet_speed
            print(self.alien_speed_factor,
                  self.fleet_drop_speed,
                  self.ship_speed_factor,
                  self.bullet_speed_factor)

