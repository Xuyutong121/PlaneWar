# file: enemy.py 文件

'''
    敌机类
'''

import pygame
import random
from gameConfig import *

class BaseEnemy(pygame.sprite.Sprite):
    '''
        敌机基本类
    '''
    def __init__(self, enemy_image, speed, multiple1, multiple2):
        '''
        :param enemy_image: 敌机图片
        :param speed: 移动速度
        :param multiple1: 距离屏幕的起点倍数
        :param multiple2: 距离屏幕的终点倍数
        '''
        pygame.sprite.Sprite.__init__(self)

        # 获取小型敌机图片
        self.image = pygame.image.load(enemy_image).convert_alpha()

        # 距离屏幕的倍数
        self.__multiple1 = multiple1
        self.__multiple2 = multiple2

        # 获取敌机尺寸
        self.rect = self.image.get_rect()

        # 计算飞机的左、上放置位置
        self.rect.left = random.randint(0, WIDTH - self.rect.width)
        self.rect.top = random.randint(self.__multiple1 * HEIGHT, self.__multiple2 * HEIGHT)

        # 设置飞机速度
        self.speed = speed

        # 设置敌机存活状态
        self.active = True

        # 标记敌机实体
        self.mask = pygame.mask.from_surface(self.image)

        # 飞机销毁图片列表
        self.destory_images = []

    def move(self):
        '''
            敌机向下移动
        :return: None
        '''
        # 检测飞机是否超出下屏幕
        if self.rect.top < HEIGHT:
            self.rect.top += self.speed
        else:
            self.reset()

    def reset(self):
        '''
            敌机重置
        :return: None
        '''
        self.active = True
        self.rect.left = random.randint(0, WIDTH - self.rect.width)
        self.rect.top = random.randint(self.__multiple1 * HEIGHT, self.__multiple2 * HEIGHT)


class SmallEnemy(BaseEnemy):
    '''
        小型敌机类
    '''
    def __init__(self):
        super().__init__(SMALL_EMEMY_IMAGE, 3, -2, 0)
        # 存储敌机摧毁图片
        self.destory_images.extend([
            pygame.image.load(S_ENEMY_DESTORY_IMAGE1).convert_alpha(),
            pygame.image.load(S_ENEMY_DESTORY_IMAGE2).convert_alpha(),
            pygame.image.load(S_ENEMY_DESTORY_IMAGE3).convert_alpha(),
            pygame.image.load(S_ENEMY_DESTORY_IMAGE4).convert_alpha()])


class MiddleEnemy(BaseEnemy):
    '''
        中型敌机类
    '''
    # 定义生命值
    life = 8

    def __init__(self):
        super().__init__(MIDDLE_EMEMY_IMAGE, 2, -5, -2)
        # 定义生命值
        self.life = MiddleEnemy.life
        # 存储敌机摧毁图片
        self.destory_images.extend([
            pygame.image.load(M_ENEMY_DESTORY_IMAGE1).convert_alpha(),
            pygame.image.load(M_ENEMY_DESTORY_IMAGE2).convert_alpha(),
            pygame.image.load(M_ENEMY_DESTORY_IMAGE3).convert_alpha(),
            pygame.image.load(M_ENEMY_DESTORY_IMAGE4).convert_alpha()])

        # 被攻击图片对象
        self.hit_image = pygame.image.load(M_ENEMY_HIT_IMAGE).convert_alpha()

        # 定义击中状态
        self.hit = False

    def reset(self):
        super().reset()
        self.life = MiddleEnemy.life

class BigEnemy(BaseEnemy):
    '''
        大型敌机类
    '''

    # 定义生命值
    life = 20

    def __init__(self):
        super().__init__(BIG_EMEMY_IMAGE1, 2, -10, -5)

        # 定义生命值
        self.life = BigEnemy.life

        # 获取大型敌机主体部分
        self.image1 = pygame.image.load(BIG_EMEMY_IMAGE2).convert_alpha()
        # 存储敌机摧毁图片
        self.destory_images.extend([
            pygame.image.load(B_ENEMY_DESTORY_IMAGE1).convert_alpha(),
            pygame.image.load(B_ENEMY_DESTORY_IMAGE2).convert_alpha(),
            pygame.image.load(B_ENEMY_DESTORY_IMAGE3).convert_alpha(),
            pygame.image.load(B_ENEMY_DESTORY_IMAGE4).convert_alpha(),
            pygame.image.load(B_ENEMY_DESTORY_IMAGE5).convert_alpha(),
            pygame.image.load(B_ENEMY_DESTORY_IMAGE6).convert_alpha()])

        # 被攻击图片对象
        self.hit_image = pygame.image.load(B_ENEMY_HIT_IMAGE).convert_alpha()

        # 定义击中状态
        self.hit = False

    def reset(self):
        super().reset()
        self.life = BigEnemy.life