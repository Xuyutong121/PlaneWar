'''
    项目视图配置
'''
import random
import sys

import pygame
from pygame.locals import *
from gameConfig import *
from gameMusic import GameMusic
from gameScreen import GameScreenManage
from gameController import GameController
from bullet import *
from gameStatus import GameStatus


class GameView(GameMusic):
    # 模块初始化
    pygame.init()
    pygame.mixer.init()

    def __init__(self):
        super().__init__()
        # 创建屏幕对象
        self.__screenManager = GameScreenManage()
        # 实例化控制器对象
        self.__controller = GameController()
        # 实例化游戏状态对象
        self.__status = GameStatus()


    def main(self):  # 主方法
        # 循环播放背景音乐
        pygame.mixer.music.play(-1)

        # 调用添加敌机方法
        self.__controller.add_enemies_manager(15, 8, 2)

        # 调用添加子弹方法
        self.__controller.add_bullet1(self.__screenManager.bullet1_number,
                                      self.__screenManager.hero.rect.midtop,
                                      Bullet1, self.__screenManager.bullet1_list)

        # 调用添加超级子弹方法
        self.__controller.add_bullet2(self.__screenManager.bullet2_number,
                                      self.__screenManager.hero,
                                      Bullet2, self.__screenManager.bullet2_list)

        while True:
            # 调用滚动屏幕方法
            self.__screenManager.screenRoll()

            for event in pygame.event.get():  # 遍历事件
                # 判断事件是否为退出
                if event.type == QUIT:
                    pygame.quit()  # 关闭游戏
                    sys.exit()  # 结束程序

                elif event.type == MOUSEBUTTONDOWN:  # 判断是否为鼠标点击事件
                    if event.button == 1 and self.__status.paused_rect.collidepoint(event.pos):  # 点击左键并在图标内
                        self.__status.puased_flag = not self.__status.puased_flag  # 切换暂停状态

                        if self.__status.puased_flag:  # 暂停游戏停止所有音效
                            pygame.time.set_timer(self.__screenManager.SUPPLY_TIMER, 0)
                            pygame.mixer.music.pause()
                            pygame.mixer.pause()
                        else:  # 非暂停情况下恢复所有音效
                            pygame.time.set_timer(self.__screenManager.SUPPLY_TIMER, 30 * 1000)
                            pygame.mixer.music.unpause()
                            pygame.mixer.unpause()

                elif event.type == MOUSEMOTION:  # 判断是否为鼠标移动事件
                    if self.__status.paused_rect.collidepoint(event.pos):  # 鼠标悬停在图标上
                        if self.__status.puased_flag:  # 暂停状态
                            self.__status.show_image = self.__status.resume_pressed_image
                        else:
                            self.__status.show_image = self.__status.pause_pressed_image
                    else:  # 鼠标未悬停在图标上
                        if self.__status.puased_flag:  # 恢复状态
                            self.__status.show_image = self.__status.resume_nor_image
                        else:
                            self.__status.show_image = self.__status.pause_nor_image

                elif event.type == KEYDOWN:  # 判断是否为按键事件
                    if event.key == K_SPACE:  # 是否按下空格键
                        if self.__screenManager.bomb_number:  # 判断超级炸弹是否还有剩余
                            self.__screenManager.bomb_number -= 1
                            self.__screenManager.bomb_sound.play()  # 播放全屏炸弹音效

                            for e in self.__controller.enemies:  # 遍历所有的敌机对象
                                if e.rect.bottom > 0:  # 判断敌机是否进入屏幕内
                                    e.active = False  # 敌机销毁

                elif event.type == self.__screenManager.SUPPLY_TIMER:  # 检测补给事件
                    # 播放补给发放音效
                    self.__screenManager.supply_sound.play()

                    # 随机选择发放补给
                    if random.choice([True, False]):
                        self.__screenManager.bomb_supply.reset()
                    else:
                        self.__screenManager.bullet_supply.reset()

                elif event.type == self.__screenManager.DOUBLE_BULLET_TIMER:  # 超级子弹检测事件
                    self.__screenManager.is_double_bullet = False
                    pygame.time.set_timer(self.__screenManager.DOUBLE_BULLET_TIMER, 0)

                elif event.type == self.__screenManager.INVINCIBLE_TIMER: # 我方飞机无敌事件检测
                    self.__screenManager.hero.invincible = False
                    pygame.time.set_timer(self.__screenManager.INVINCIBLE_TIMER, 0)

            if self.__screenManager.game_running:   # 开始游戏
                pygame.time.set_timer(self.__screenManager.SUPPLY_TIMER, 0)
                self.__screenManager.gameStarting()
            else:
                if self.__screenManager.hero.life:
                    if not self.__status.puased_flag:
                        # 绘制子弹
                        self.__screenManager.bulletDraw(self.__controller.enemies, self.__controller.middle_enemies,
                                                        self.__controller.big_enemies)

                        # 绘制飞机
                        self.__screenManager.planeDraw()

                        # 控制飞机移动
                        self.__screenManager.controlPlaneMove()
                        # self.__screenManager.mouseControlPlaneMove()

                        # 绘制敌机
                        self.__screenManager.enemyDraw(self.__controller.big_enemies, self.__controller.middle_enemies,
                                                       self.__controller.small_enemies, self.__controller.enemies,
                                                       self.__controller.bloodDraw)

                        # 游戏等级提升
                        self.__controller.game_level_upgrade(self.__screenManager.score, self.upgrade_sound)

                        # 调用暂停不显示的功能
                        self.__screenManager.elementHideDraw()

                        # 绘制补给
                        self.__screenManager.supplyDraw()

                    # 元素显示绘制
                    self.__screenManager.elementDisplayDraw(self.__status.show_image, self.__status.paused_rect)

                # 游戏结束画面
                elif self.__screenManager.hero.life == 0:
                    # 调用结束画面
                    self.__screenManager.gameOverDraw(self.main, self.__controller.small_enemies, self.__controller.middle_enemies, self.__controller.big_enemies, self.__controller.enemies)

            # 设置屏幕的刷新频率
            self.__screenManager.clock.tick(60)

            # 更新窗口
            pygame.display.update()
