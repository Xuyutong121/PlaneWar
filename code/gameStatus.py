'''
    游戏暂停/恢复状态
'''
from gameConfig import *
import pygame

class GameStatus:
    def __init__(self):
        # 定义暂停未选中图片对象
        self.pause_nor_image = pygame.image.load(PAUSE_NOR).convert_alpha()
        # 定义暂停选中图片对象
        self.pause_pressed_image = pygame.image.load(PAUSE_PRESSED).convert_alpha()
        # 定义恢复未选中图片对象
        self.resume_nor_image = pygame.image.load(RESUME_NOR).convert_alpha()
        # 定义暂停选中图片对象
        self.resume_pressed_image = pygame.image.load(RESUME_PRESSED).convert_alpha()

        # 定义图片位置
        self.paused_rect = self.pause_pressed_image.get_rect()
        self.paused_rect.left = WIDTH - self.paused_rect.width - 10
        self.paused_rect.top = 10

        # 定义显示图片
        self.show_image = self.pause_nor_image

        # 定义暂停游戏状态
        self.puased_flag = False