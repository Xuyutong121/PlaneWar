from enemy import *


class GameController:
    def __init__(self):
        # 生成敌方飞机管理组
        self.enemies = pygame.sprite.Group()
        # 生成小型敌机管理组
        self.small_enemies = pygame.sprite.Group()
        # 生成中型敌机管理组
        self.middle_enemies = pygame.sprite.Group()
        # 生成大型敌机管理组
        self.big_enemies = pygame.sprite.Group()
        # 定义游戏级别
        self.__level = 1

    def add_enemies(self, enemy, enemy_group, count):
        '''
            添加大中小型飞机到飞机管理组中
        :param enemy: 大中小飞机类
        :param enemy_group: 大中小飞机管理组
        :param count: 添加数量
        :return: None
        '''
        for i in range(count):
            each_enemy = enemy()  # 实例化大中小飞机对象
            self.enemies.add(each_enemy)  # 添加到飞机管理组
            enemy_group.add(each_enemy)  # 添加敌机到敌机管理组

    def add_enemies_manager(self, small_count, middle_count, big_count):
        '''
            增加敌机管理
        :param small_count: 小型敌机数量
        :param middle_count: 中型敌机数量
        :param big_count: 大型敌机数量
        :return: None
        '''
        # 添加小型敌机
        self.add_enemies(SmallEnemy, self.small_enemies, small_count)
        # 添加中型敌机
        self.add_enemies(MiddleEnemy, self.middle_enemies, middle_count)
        # 添加大型敌机
        self.add_enemies(BigEnemy, self.big_enemies, big_count)

    def add_bullet1(self, number, postion, bullet, bullet_list):
        '''
            添加普通子弹
        :param number: 子弹数量
        :param postion: 子弹位置
        :param bullet: 子弹类
        :param bullet_list: 子弹列表
        :return:
        '''
        for i in range(number):
            bullet1 = bullet(postion)
            bullet_list.append(bullet1)

    def add_bullet2(self, number, hero, bullet, bullet_list):
        '''
            添加超级子弹
        :param number: 子弹数量
        :param hero: 英雄飞机对象（基于飞机定位）
        :param bullet: 子弹类
        :param bullet_list: 子弹列表
        :return:
        '''
        for i in range(number // 2):
            bullet21 = bullet((hero.rect.centerx - 33, hero.rect.centery))
            bullet22 = bullet((hero.rect.centerx + 30, hero.rect.centery))
            bullet_list.append(bullet21)
            bullet_list.append(bullet22)

    def bloodDraw(self, screen, enemy, Enemy):
        '''
           绘制大、中型敌机血条
        :param screen: 屏幕对象
        :param enemy: 敌机对象
        :param Enemy: 中/大型敌机类
        :return: None
        '''
        # 绘制血量背景
        pygame.draw.line(screen, BLACK,
                         (enemy.rect.left, enemy.rect.top - 5),
                         (enemy.rect.right, enemy.rect.top - 5), 2)

        # 当生命值大于20%时显示绿色，否则显示红色
        life_remain = enemy.life / Enemy.life
        if life_remain > 0.2:
            life_color = GREEN
        else:
            life_color = RED

        # 绘制血条
        pygame.draw.line(screen, life_color,
                         (enemy.rect.left, enemy.rect.top - 5),
                         (enemy.rect.left + enemy.rect.width * life_remain, enemy.rect.top - 5), 2)

    def __enemy_speed_increase(self, target, inc):
        '''
            敌机增加速度
        :param target: 敌机对象列表
        :param inc: 速度值
        :return: None
        '''
        for each in target:
            each.speed += inc

    def game_level_upgrade(self, score, upgrade_sound):
        '''
            游戏难度设置
        :param score: 分数
        :param upgrade_sound: 升级音效
        :return: None
        '''
        if self.__level == 1 and score > 5000:
            self.__level = 2
            upgrade_sound.play()
            # 增加3架小型敌机，2架中型敌机，1架大型敌机
            self.add_enemies_manager(3, 2, 1)
            # 提升敌机速度
            self.__enemy_speed_increase(self.small_enemies, 1)
        elif self.__level == 2 and score > 30000:
            self.__level = 3
            upgrade_sound.play()
            # 增加5架小型敌机，3架中型敌机，2架大型敌机
            self.add_enemies_manager(5, 3, 2)
            # 提升敌机速度
            self.__enemy_speed_increase(self.small_enemies, 1)
            self.__enemy_speed_increase(self.middle_enemies, 1)
        elif self.__level == 3 and score > 200000:
            self.__level = 4
            upgrade_sound.play()
            # 增加5架小型敌机，3架中型敌机，2架大型敌机
            self.add_enemies_manager(5, 3, 2)
            # 提升敌机速度
            self.__enemy_speed_increase(self.small_enemies, 1)
            self.__enemy_speed_increase(self.middle_enemies, 1)
        elif self.__level == 4 and score > 500000:
            self.__level = 5
            upgrade_sound.play()
            # 增加5架小型敌机，3架中型敌机，2架大型敌机
            self.add_enemies_manager(5, 3, 2)
            # 提升敌机速度
            self.__enemy_speed_increase(self.small_enemies, 1)
            self.__enemy_speed_increase(self.middle_enemies, 1)

        print(f"升到：{self.__level} 级")