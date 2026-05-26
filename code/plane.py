'''
    飞机类
'''

import pygame
from GameConfig import PLANE1_IMG, PLANE2_IMG, HEIGHT, WIDTH

class Plane(pygame.sprite.Sprite):   # 继承精灵类（用于碰撞检测）
    def __init__(self):
        super().__init__()
        # self.image1 = pygame.image.load(PLANE1_IMG).convert_alpha()  # 获取飞机的实体部分
        self.image1 = pygame.image.load(PLANE1_IMG)
        self.image2 = pygame.image.load(PLANE2_IMG)
        # 获取飞机的尺寸
        self.rect = self.image1.get_rect()
        # 定义飞机放置位置
        self.rect.left = (WIDTH - self.rect.width) //  2
        self.rect.top = HEIGHT - 60 - self.rect.height
        # 定义飞机飞行的速度
        self.speed = 10
        
    def moveUp(self):
        '''
            向上移动
        :return: None
        '''
        # 判断飞机是否超出屏幕外
        if self.rect.top > 0:
            self.rect.top -= self.speed
        else:
            self.rect.top = 0
    
    def moveDown(self):
        '''
            向下移动
        :return: None
        '''
        # 判断飞机是否超出屏幕外
        if self.rect.bottom < HEIGHT - 60:
            self.rect.top += self.speed
        else:
            self.rect.bottom = HEIGHT - 60
    
    def moveLeft(self):
        '''
            向左移动
        :return: None
        '''
        # 判断飞机是否超出屏幕外
        if self.rect.left > 0:
            self.rect.left -= self.speed
        else:
            self.rect.left = 0
    
    def moveRight(self):
        '''
            向右移动
        :return: None
        '''
        # 判断飞机是否超出屏幕外
        if self.rect.right < WIDTH:
            self.rect.right += self.speed
        else:
            self.rect.right = WIDTH