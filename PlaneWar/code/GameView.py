# 游戏界面显示
import sys
import pygame
from GameConfig import *
from GameMusic import GameMusic
from plane import Plane

class ScreenImages:
    def __init__(self):
        # 读取背景图片
        self.__bg_img = pygame.image.load(BG_IMG)
        # 读取logo图片
        self.__icon_img = pygame.image.load(ICON_IMG)
    
    @property
    def icon_img(self):
        return self.__icon_img
    
    @property
    def bg_img(self):
        return self.__bg_img


class GameScreenManager(ScreenImages):
    def __init__(self):
        super().__init__()
        # 创建窗口: 大小 480*852
        self.__screen = pygame.display.set_mode(SCREEN_SIZE)
        # 设置窗口图标
        pygame.display.set_caption("飞机大战 3.0")
        # 设置窗口LOGO
        pygame.display.set_icon(self.icon_img)
        # 实例化飞机对象
        self.hero = Plane()
    
    def draw_plane(self):   # 绘制飞机
        self.__screen.blit(self.hero.image1, self.hero.rect)
    
    def control_plane(self):  # 通过键盘控制飞机的移动
        # 1 检测用户是否进行键盘操作事件
        self.__key_pressed = pygame.key.get_pressed()
        
        # 2 判断用户的按键，调用飞机对应的方法
        if self.__key_pressed[pygame.K_w] or self.__key_pressed[pygame.K_UP]:
            self.hero.moveUp()
        elif self.__key_pressed[pygame.K_s] or self.__key_pressed[pygame.K_DOWN]:
            self.hero.moveDown()
        elif self.__key_pressed[pygame.K_a] or self.__key_pressed[pygame.K_LEFT]:
            self.hero.moveLeft()
        elif self.__key_pressed[pygame.K_d] or self.__key_pressed[pygame.K_RIGHT]:
            self.hero.moveRight()
        
    @property
    def screen(self):  # 只读模式
        return self.__screen


class GameView(GameMusic):
    # 模块与音乐模块的初始化
    pygame.init()
    pygame.mixer.init()
    
    def __init__(self):
        super().__init__()
        self.__manager = GameScreenManager()
    
    def main(self):
        # 循环播放背景音乐
        pygame.mixer.music.play(-1)
        while True:
            # 加载背景图（背景图、位置以原点位置平铺）
            self.__manager.screen.blit(self.__manager.bg_img, (0, 0))
            # 调用绘制飞机的方法
            self.__manager.draw_plane()
            # 调用控制飞机的方法
            self.__manager.control_plane()
            
            # 遍历窗口操作事件
            for event in pygame.event.get():
                # 关闭窗口：判断是否是关闭窗口的事件
                if event.type == pygame.QUIT:
                    pygame.quit()  # 退出游戏
                    sys.exit()  # 结束程序
            
            # 更新窗口
            pygame.display.update()
