'''
    子弹类
'''
import pygame
from gameConfig import *


class BaseBullet(pygame.sprite.Sprite):
    '''
        单发子弹类
    '''

    def __init__(self, position, image, speed):
        '''
            初始化子弹类
        :param position: 子弹位置
        :param image: 子弹图片
        :param speed: 子弹速度
        '''
        pygame.sprite.Sprite.__init__(self)

        # 创建子弹对象
        self.image = pygame.image.load(image).convert_alpha()

        # 获取图片尺寸
        self.rect = self.image.get_rect()

        # 初始化子弹位置
        self.rect.left, self.rect.top = position

        # 设置子弹移动速度
        self.speed = speed

        # 设置子弹存活状态
        self.active = True

        # 设置子弹主体，实现完美碰撞
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        '''
            子弹移动方法
        :return: None
        '''
        self.rect.top -= self.speed

        if self.rect.top < 0:
            self.active = False


    def reset(self, postion):
        '''
            子弹重置方法
        :return:None
        '''
        self.active = True
        self.rect.left, self.rect.top = postion


class Bullet1(BaseBullet):
    '''
        普通子弹类
    '''
    def __init__(self, postion):
        super().__init__(postion, BUTTLE1_IMAGE, 12)

class Bullet2(BaseBullet):
    '''
        超级子弹类
    '''

    def __init__(self, postion):
        super().__init__(postion, BUTTLE2_IMAGE, 14)
