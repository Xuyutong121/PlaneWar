'''
    补给类
'''

import pygame
from gameConfig import *
import random


class BaseSupply(pygame.sprite.Sprite):
    '''
        补给基类
    '''
    def __init__(self, image):
        super().__init__()

        # 创建超级子弹图片对象
        self.image = pygame.image.load(image).convert_alpha()
        # 获取超级子弹尺寸
        self.rect = self.image.get_rect()
        # 设置子弹的位置
        self.rect.left, self.rect.bottom = random.randint(0, WIDTH - self.rect.width), -100
        # 定义子弹速度
        self.speed = 5
        # 定义子弹存活状态
        self.active = False
        # 定义实体
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        '''
            子弹移动
        :return: None
        '''
        if self.rect.top < HEIGHT:
            self.rect.top += self.speed
        else:
            self.active = False

    def reset(self):
        '''
            子弹重置
        :return: None
        '''
        self.active = True
        self.rect.left, self.rect.bottom = random.randint(0, WIDTH - self.rect.width), -100


class Bullte_Supply(BaseSupply):
    '''
        超级子弹类
    '''
    def __init__(self):
        super().__init__(PROP1_IMAGE)


class Bomb_Supply(BaseSupply):
    '''
        超级炸弹类
    '''
    def __init__(self):
        super().__init__(PROP2_IMAGE)
