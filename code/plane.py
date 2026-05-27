'''
    飞机类
'''
import pygame
from gameConfig import *


class Plane(pygame.sprite.Sprite):  # 继承精灵类（用于碰撞检测）
    def __init__(self):
        # 调用精灵类的初始化方法
        super().__init__()

        # 飞机图片对象：将图片转化为Surface对象，保留了图像的 Alpha 通道(8位的灰度通道，该通道用256级灰度来记录图像中的透明度信息)
        # self.image = pygame.image.load(PLANE_IMAGE).convert_alpha()
        self.image1 = pygame.image.load(PLANE_IMAGE1).convert_alpha()  # 会自动转换为Surface对象，保留了图像的 Alpha 通道
        self.image2 = pygame.image.load(PLANE_IMAGE2).convert_alpha()   # 会自动转换为Surface对象，保留了图像的 Alpha 通道

        # 获取图片矩形的位置和大小信息（left/right/top/bottom，width/height)
        self.rect = self.image1.get_rect()

        # 定义飞机的左、上放置位置
        self.rect.left = (WIDTH - self.rect.width) // 2
        self.rect.top = HEIGHT - self.rect.height - 60

        # 设置飞机速度
        self.speed = 10

        # 定义飞机存活状态
        self.active = True

        # 定义飞机生命
        self.life = 3

        # 定义标记飞机实体
        self.mask = pygame.mask.from_surface(self.image1)

        # 飞机销毁图片
        self.destory_images = []
        self.destory_images.extend([
            pygame.image.load(PLANE_DESTORY_IMAGE1).convert_alpha(),
            pygame.image.load(PLANE_DESTORY_IMAGE2).convert_alpha(),
            pygame.image.load(PLANE_DESTORY_IMAGE3).convert_alpha(),
            pygame.image.load(PLANE_DESTORY_IMAGE4).convert_alpha()])

        # 定义飞机无敌状态
        self.invincible = False

    def moveUp(self):
        '''
            向上移动
        :return: None
        '''
        if self.rect.top > 0:  # 未超出上边界
            self.rect.top -= self.speed
        else:  # 超出上边界
            self.rect.top = 0

    def moveDown(self):
        '''
            向下移动
        :return: None
        '''
        if self.rect.bottom < HEIGHT - 60:  # 未超出下边界
            self.rect.top += self.speed
        else:  # 超出下边界
            self.rect.bottom = HEIGHT - 60

    def moveLeft(self):
        '''
            向左移动
        :return: None
        '''
        if self.rect.left > 0:  # 未超出左边界
            self.rect.left -= self.speed
        else:  # 超出左边界
            self.rect.left = 0

    def moveRight(self):
        '''
            向右移动
        :return: None
        '''
        if self.rect.right < WIDTH:  # 未超出右边界
            self.rect.right += self.speed
        else:  # 超出右边界
            self.rect.right = WIDTH


    def move(self, postition):
        '''
            鼠标控制飞机移动
        :return: None
        '''
        self.rect.left, self.rect.top = postition
        if self.rect.right <= WIDTH:
            self.rect.right += self.speed
        else:
            self.rect.right = WIDTH

        if self.rect.bottom < HEIGHT - 60:
            self.rect.bottom += self.speed
        else:
            self.rect.bottom = HEIGHT - 60


    def reset(self):
        '''
            我方飞机重置
        :return: None
        '''
        self.active = True
        self.invincible = True
        self.rect.left = (WIDTH - self.rect.width) // 2
        self.rect.top = HEIGHT - self.rect.height - 60