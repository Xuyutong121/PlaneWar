'''
    项目窗口配置
'''
import sys

import pygame
from pygame.locals import *
from gameConfig import *
from gameMusic import GameMusic
from plane import Plane
from enemy import *
from supply import *

class SreemImages:
    '''
        屏幕图像管理
    '''

    def __init__(self):
        # 读取背景图片
        self.__bg_image1 = pygame.image.load(BG_IMAGE)
        self.__bg_image2 = pygame.image.load(BG_IMAGE)

        # 读取图标图片
        self.__icon_image = pygame.image.load(ICON_IMAGE)
        # 字体
        self.__font_type = pygame.font.Font(FONT_PATH, 38)
        # 超级炸弹图片对象
        self.bomb_image = pygame.image.load(BOMB_IMAGE)
        # 我方飞机生命值图片
        self.hero_life_image = pygame.image.load(LIFE_IMAGE)
        self.hero_life_rect = self.hero_life_image.get_rect()

        # 结束游戏图片
        self.gameover_image = pygame.image.load(GAMEOVER_IMAGE)

        # 重新游戏图片
        self.gameAgain_image = pygame.image.load(RESTART_IMAGE)

        # 游戏标题图片
        self.gameName = pygame.image.load(TITLE_IMAGE)

        # 开始游戏图片
        self.gameStart = pygame.image.load(START_IMAGE)

        # 加载游戏图片
        self.gameLoad1 = pygame.image.load(LOADING_IMAGE1)
        self.gameLoad2 = pygame.image.load(LOADING_IMAGE2)
        self.gameLoad3 = pygame.image.load(LOADING_IMAGE3)
        self.gameLoad4 = pygame.image.load(LOADING_IMAGE4)

    @property
    def bg_image1(self):  # 背景图只读模式
        return self.__bg_image1

    @property
    def bg_image2(self):  # 背景图只读模式
        return self.__bg_image2

    @property
    def icon_image(self):  # 图标图只读模式
        return self.__icon_image

    @property
    def font_type(self):  # 只读模式
        return self.__font_type


class GameScreenManage(SreemImages, GameMusic):
    def __init__(self):
        super().__init__()
        GameMusic.__init__(self)

        # 创建窗口
        self.__screen = pygame.display.set_mode(SCREEN_SIZE)

        # 设置图标
        pygame.display.set_icon(self.icon_image)

        # 设置窗口标题
        pygame.display.set_caption("飞机大战 OO版")

        # 背景图初始位置
        self.__bg_image_y = 0

        # 背景图移动速度
        self.__bg_roll_speed = 1

        # 定义游戏时钟
        self.clock = pygame.time.Clock()

        # 定义背景切换标志
        self.__change_flag = True

        # 实例化飞机对象
        self.hero = Plane()

        # 定义计数器
        self.__delay = 100

        # 定义飞机切换
        self.__image_switch = True

        # 定义我方飞机爆炸图片切换索引
        self.__plane_destory_index = 0

        # 定义小型敌机爆炸图片切换索引
        self.__sEnemy_destory_index = 0

        # 定义中型敌机爆炸图片切换索引
        self.__mEnemy_destory_index = 0

        # 定义中型敌机爆炸图片切换索引
        self.__bEnemy_destory_index = 0

        # 存放普通子弹
        self.bullet1_list = []
        self.__bullet1_index = 0  # 普通子弹索引
        self.bullet1_number = 4  # 普通子弹数量

        # 定义分数
        self.__score = 0

        # 定义全屏炸弹的数量
        self.bomb_number = 3

        # 实例化补给对象
        self.bullet_supply = Bullte_Supply()
        self.bomb_supply = Bomb_Supply()

        # 创建补给定时器
        self.SUPPLY_TIMER = USEREVENT
        # 设置补给定时30秒：发放补给
        pygame.time.set_timer(self.SUPPLY_TIMER, 30 * 1000)

        # 定义超级子弹定时器
        self.DOUBLE_BULLET_TIMER = USEREVENT + 1

        # 定义是否使用超级子弹
        self.is_double_bullet = False

        # 存放超级子弹
        self.bullet2_list = []
        self.__bullet2_index = 0  # 超级子弹索引
        self.bullet2_number = 4  # 超级子弹数量

        # 解除我方飞机无敌定时器
        self.INVINCIBLE_TIMER = USEREVENT + 2

        # 定义文件打开限制标识
        self.__recorded = False

        # 定义结束文字格式
        self.__font_types = pygame.font.Font(FONT_PATH, 48)

        # 存储游戏加载图片
        self.__gameLoad_list = [self.gameLoad1, self.gameLoad2, self.gameLoad3, self.gameLoad4]

        # 游戏加载图片索引
        self.__gameload_index = 0

        # 定义游戏开始状态
        self.game_running = True

    @property
    def score(self):
        return self.__score

    def screenRoll(self):
        '''
            屏幕滚动
        :param screen: 屏幕对象
        :return: None
        '''
        # 修改背景图移动
        self.__bg_image_y += self.__bg_roll_speed

        # 判断背景图是否超出边界，超出重置到初始位置
        if self.__change_flag:  # 图片1超出屏幕下边界
            self.__screen.blit(self.bg_image2, (0, self.__bg_image_y))
            self.__screen.blit(self.bg_image1, (0, self.__bg_image_y - HEIGHT))
        else:  # 图片2超出屏幕下边界
            self.__screen.blit(self.bg_image1, (0, self.__bg_image_y))
            self.__screen.blit(self.bg_image2, (0, self.__bg_image_y - HEIGHT))

        # 当背景图全部超出屏幕，重置y轴的位置
        if self.__bg_image_y > HEIGHT:
            self.__change_flag = not self.__change_flag
            self.__bg_image_y = 0

    def controlPlaneMove(self):
        '''
            控制飞机移动
        :return: None
        '''
        # 检测用户键盘操作
        self.__key_pressed = pygame.key.get_pressed()

        # 控制WSAD/方向键控制飞机移动
        if self.__key_pressed[K_w] or self.__key_pressed[K_UP]:
            self.hero.moveUp()
        elif self.__key_pressed[K_s] or self.__key_pressed[K_DOWN]:
            self.hero.moveDown()
        elif self.__key_pressed[K_a] or self.__key_pressed[K_LEFT]:
            self.hero.moveLeft()
        elif self.__key_pressed[K_d] or self.__key_pressed[K_RIGHT]:
            self.hero.moveRight()

    def mouseControlPlaneMove(self):
        '''
            鼠标控制飞机移动
        :return: None
        '''
        self.__mouse_pos = pygame.mouse.get_pos()
        self.hero.move(self.__mouse_pos)

    def planeDraw(self):
        '''
            飞机绘制
        :return: None
        '''
        # 修改飞机切换状态
        if not self.__delay % 10:
            self.__image_switch = not self.__image_switch

        if self.hero.active:  # 飞机存活
            if self.__image_switch:
                self.__screen.blit(self.hero.image1, self.hero.rect)
            else:
                self.__screen.blit(self.hero.image2, self.hero.rect)
        else:  # 飞机被销毁
            self.hero_down_sound.play()  # 播放我方飞机销毁音乐
            # 每3帧切换一次爆炸图片
            if not self.__delay % 3:
                # 绘制销毁图片
                self.__screen.blit(self.hero.destory_images[self.__plane_destory_index], self.hero.rect)
                # 修改销毁图片索引
                self.__plane_destory_index = (self.__plane_destory_index + 1) % 4
                # 播放销毁图片完毕后，重置
                if self.__plane_destory_index == 0:
                    self.hero.life -= 1
                    self.hero.reset()
                    pygame.time.set_timer(self.INVINCIBLE_TIMER, 5 * 1000)

        self.__delay -= 1

        if not self.__delay:
            self.__delay = 100

    def enemyDraw(self, big_enemies, middle_enemies, small_enemies, enemies, blood_draw):
        '''
            绘制敌机
        :param big_enemies: 大型敌机精灵组
        :param middle_enemy: 中型敌机精灵组
        :param small_enemies: 小型敌机精灵组
        :param enemies: 大中小型敌机精灵组
        :param blood_draw: 血条绘制方法
        :return: None
        '''
        # 绘制大型敌机
        for each in big_enemies:
            if each.active:  # 飞机存活
                each.move()  # 敌机移动

                # 绘制血条
                blood_draw(self.__screen, each, BigEnemy)

                if each.hit:  # 被击中
                    self.__screen.blit(each.hit_image, each.rect)
                    each.hit = False
                else:
                    # 大型敌机动画切换
                    if self.__image_switch:
                        self.__screen.blit(each.image, each.rect)
                    else:
                        self.__screen.blit(each.image1, each.rect)

                # 加载大型敌机入场音乐
                if each.rect.bottom == -50:
                    self.enemy3_fly_sound.play(-1)

            else:  # 敌机被摧毁
                if not (self.__delay % 3):  # 每3帧切换销毁图片
                    if self.__bEnemy_destory_index == 0:  # 只播放一次
                        self.enemy3_down_sound.play()  # 播放大型敌机销毁音乐

                    # 绘制销毁图片
                    self.__screen.blit(each.destory_images[self.__bEnemy_destory_index], each.rect)

                    # 修改销毁图片索引
                    self.__bEnemy_destory_index = (self.__bEnemy_destory_index + 1) % 6

                    # 播放销毁图片完毕后，重置
                    if self.__bEnemy_destory_index == 0:
                        self.enemy3_fly_sound.stop()  # 停止飞机入场播放
                        self.__score += 1500
                        each.reset()  # 重置大型敌机

        # 绘制中型敌机
        for each in middle_enemies:
            if each.active:  # 飞机存活
                each.move()  # 敌机移动

                # 绘制血条
                blood_draw(self.__screen, each, MiddleEnemy)

                if each.hit:  # 被击中
                    self.__screen.blit(each.hit_image, each.rect)
                    each.hit = False
                else:
                    # 中型敌机绘制
                    self.__screen.blit(each.image, each.rect)
            else:  # 敌机被摧毁
                if not (self.__delay % 3):  # 每3帧切换销毁图片
                    if self.__mEnemy_destory_index == 0:  # 只播放一次
                        self.enemy2_down_sound.play()  # 播放中型敌机销毁音乐

                    # 绘制销毁图片
                    self.__screen.blit(each.destory_images[self.__mEnemy_destory_index], each.rect)

                    # 修改销毁图片索引
                    self.__mEnemy_destory_index = (self.__mEnemy_destory_index + 1) % 4

                    # 播放销毁图片完毕后，重置
                    if self.__mEnemy_destory_index == 0:
                        self.__score += 800
                        each.reset()  # 重置中型敌机

        # 绘制小型敌机
        for each in small_enemies:
            if each.active:  # 飞机存活
                each.move()  # 敌机移动

                # 小型敌机动画切换
                self.__screen.blit(each.image, each.rect)
            else:  # 敌机被摧毁
                if not (self.__delay % 3):  # 每3帧切换销毁图片
                    if self.__sEnemy_destory_index == 0:  # 只播放一次
                        self.enemy1_down_sound.play()  # 播放中型敌机销毁音乐

                    # 绘制销毁图片
                    self.__screen.blit(each.destory_images[self.__sEnemy_destory_index], each.rect)

                    # 修改销毁图片索引
                    self.__sEnemy_destory_index = (self.__sEnemy_destory_index + 1) % 4

                    # 播放销毁图片完毕后，重置
                    if self.__sEnemy_destory_index == 0:
                        self.__score += 600
                        each.reset()  # 重置小型敌机

        self.__enemies_down = pygame.sprite.spritecollide(self.hero, enemies, False, pygame.sprite.collide_mask)

        if self.__enemies_down and not self.hero.invincible:
            self.hero.active = False  # 我方飞机销毁
            for e in self.__enemies_down:  # 遍历被碰撞的敌机
                e.active = False  # 敌机销毁

    def bulletDraw(self, enemies, middle_enemies, big_enemies):
        '''
            绘制子弹
        :param eneies: 所有类型的敌机组
        :param middle_enemies: 中型敌机组
        :param big_enemies: 大型敌机组
        :return: None
        '''
        # 修改子弹索引
        if not self.__delay % 10:
            self.bullet_sound.play()
            if self.is_double_bullet:
                self.__bullets = self.bullet2_list
                self.__bullets[self.__bullet2_index].reset((self.hero.rect.centerx-33, self.hero.rect.centery))
                self.__bullets[self.__bullet2_index+1].reset((self.hero.rect.centerx+30, self.hero.rect.centery))
                self.__bullet2_index = (self.__bullet2_index + 2) % self.bullet2_number
            else:
                self.__bullets = self.bullet1_list
                self.__bullets[self.__bullet1_index].reset(self.hero.rect.midtop)
                self.__bullet1_index = (self.__bullet1_index + 1) % self.bullet1_number


        try:
            # 绘制子弹
            for b in self.__bullets:
                if b.active:
                    b.move()
                    self.__screen.blit(b.image, b.rect)


                    # 子弹与敌机发生碰撞
                    self.__enemy_collide = pygame.sprite.spritecollide(b, enemies, False, pygame.sprite.collide_mask)

                    if self.__enemy_collide:  # 存在碰撞对象，则将子弹/敌机状态修改为False
                        b.active = False
                        for e in self.__enemy_collide:  # 遍历被碰撞的敌机对象
                            if e in middle_enemies or e in big_enemies:  # 判断是否为中大型敌机
                                e.life -= 1  # 敌机生命值减少1
                                e.hit = True  # 敌机被击中
                                if e.life == 0:  # 无生命值则毁灭
                                    e.active = False
                            else:
                                e.active = False  # 小型飞机直接毁灭
        except Exception as e:
            pass

    def elementDisplayDraw(self, show_image, show_image_rect):
        '''
            绘制暂停显示元素
        :param show_image: 暂停/恢复游戏图片
        :param show_image_rect: 暂停/恢复游戏图片位置
        :return: None
        '''
        # 分数绘制
        # 设置文本样式（文本内容、抗锯齿，白色）
        self.__score_text = self.font_type.render(f"Score : {self.__score}", True, WHITE)
        # 加载字体
        self.__screen.blit(self.__score_text, (10, 5))

        # 绘制暂停/恢复游戏
        self.__screen.blit(show_image, show_image_rect)

    def elementHideDraw(self):
        '''
            暂停游戏隐藏元素绘制
        :return: None
        '''
        # 绘制全屏炸弹
        self.__bomb_text = self.font_type.render(f" x {self.bomb_number}", True, WHITE)
        self.__bomb_text_rect = self.__bomb_text.get_rect()
        self.__screen.blit(self.bomb_image, (10, HEIGHT - 10 - self.bomb_image.get_rect().height))
        self.__screen.blit(self.__bomb_text, (10 + self.bomb_image.get_rect().width, HEIGHT - 15 - self.__bomb_text_rect.height))

        # 绘制剩余生命
        if self.hero.life:
            for i in range(self.hero.life):
                self.__screen.blit(self.hero_life_image, ((WIDTH - 10 - (i + 1) * self.hero_life_rect.width),
                                 HEIGHT - 10 - self.hero_life_rect.height))

    def supplyDraw(self):
        '''
            绘制补给
        :return: None
        '''
        # 超级炸弹绘制
        if self.bomb_supply.active:
            self.bomb_supply.move()
            self.__screen.blit(self.bomb_supply.image, self.bomb_supply.rect)

            # 检测我方飞机是否与补给发生碰撞
            if pygame.sprite.collide_mask(self.bomb_supply, self.hero):
                # 播放获得超级炸弹音效
                self.get_bomb_sound.play()
                # 当超级炸弹数量小于3个，则加1
                if self.bomb_number < 3:
                    self.bomb_number += 1

                self.bomb_supply.active = False

        # 超级子弹绘制
        if self.bullet_supply.active:  # 超级子弹存活绘制
            self.bullet_supply.move()
            self.__screen.blit(self.bullet_supply.image, self.bullet_supply.rect)

            # 检测我方飞机是否与补给发生碰撞
            if pygame.sprite.collide_mask(self.bullet_supply, self.hero):
                # 播放获得超级炸弹音效
                self.get_bullet_sound.play()
                # 发射超级子弹
                self.is_double_bullet = True
                pygame.time.set_timer(self.DOUBLE_BULLET_TIMER, 18 * 1000)
                self.bullet_supply.active = False

    def gameOverDraw(self, startgame, small_enemies, middle_enemies, big_enemies, enemies):
        '''
            游戏结束界面绘制
        :param startgame: 游戏开始主方法
        :param small_enemies: 小敌机组
        :param middle_enemies: 中敌机组
        :param big_enemies: 大敌机组
        :param enemies: 大中小敌机组
        :return: None
        '''
        # 关闭声音
        pygame.mixer.music.stop()
        pygame.mixer.stop()

        # 停止发放补给
        pygame.time.set_timer(self.SUPPLY_TIMER, 0)

        if not self.__recorded:
            self.__recorded = True
            # 读取历史最高分
            with open("record.txt", 'r') as f:
                self.__record_score = int(f.read())

            # 如果玩家的分数高于历史最高分，则存档
            if self.__score > self.__record_score:
                with open("record.txt", 'w') as f:
                    f.write(str(self.__score))

        # 结束界面绘制
        # 绘制最好成绩
        self.__record_text = self.__font_types.render(f"Best: {self.__record_score}", True, WHITE)
        self.__screen.blit(self.__record_text, (50, 50))

        # 绘制本次游戏成绩
        self.__your_score_texts = self.__font_types.render(f"Your Score: ", True, WHITE)
        self.__your_score_texts_rect = self.__your_score_texts.get_rect()
        self.__your_score_texts_rect.left = (WIDTH - self.__your_score_texts_rect.width) // 2
        self.__your_score_texts_rect.top = HEIGHT // 2 - 100
        self.__screen.blit(self.__your_score_texts, self.__your_score_texts_rect)

        self.__score_texts = self.__font_types.render(str(self.__score), True, WHITE)
        self.__score_texts_rect = self.__score_texts.get_rect()
        self.__score_texts_rect.left = (WIDTH - self.__your_score_texts_rect.width) // 2
        self.__score_texts_rect.top = self.__your_score_texts_rect.bottom + 10
        self.__screen.blit(self.__score_text, self.__score_texts_rect)

        # 绘制重新开始游戏按钮
        self.__again_rect = self.gameAgain_image.get_rect()
        self.__again_rect.left =(WIDTH - self.__again_rect.width) // 2
        self.__again_rect.top = self.__score_texts_rect.bottom + 50
        self.__screen.blit(self.gameAgain_image, self.__again_rect)

        # 绘制结束开始游戏按钮
        self.__gameOver_rect = self.gameover_image.get_rect()
        self.__gameOver_rect.left =(WIDTH - self.__again_rect.width) // 2
        self.__gameOver_rect.top = self.__again_rect.bottom + 20
        self.__screen.blit(self.gameover_image, self.__gameOver_rect)

        # 检测用户的鼠标操作
        if pygame.mouse.get_pressed()[0]:  # 用户按下鼠标左键
            # 获取鼠标位置
            self.__pos = pygame.mouse.get_pos()
            # 用户点击：重新开始
            if self.__again_rect.left < self.__pos[0] < self.__again_rect.right and self.__again_rect.top < self.__pos[1] < self.__again_rect.bottom:
                self.hero.life = 3    # 恢复生命值
                self.__score = 0   # 分数重置
                small_enemies.empty()   # 清空小敌机组
                middle_enemies.empty()  # 清空中敌机组
                big_enemies.empty()  # 清空大敌机组
                enemies.empty()  # 清空大中小敌机组
                startgame()  # 调用main方法

            elif self.__gameOver_rect.left < self.__pos[0] < self.__gameOver_rect.right and self.__gameOver_rect.top < self.__pos[1] < self.__gameOver_rect.bottom:
                pygame.quit()
                sys.exit()

    def gameStarting(self):
        '''
            游戏开始
        :return:
        '''
        # 绘制游戏标题
        self.__screen.blit(self.gameName, ((WIDTH - self.gameName.get_rect().width)//2, HEIGHT // 5))

        # 绘制加载动画
        self.__screen.blit(self.__gameLoad_list[self.__gameload_index], (self.__gameLoad_list[self.__gameload_index].get_rect().width + (self.__gameload_index + 1) * 10, HEIGHT // 3 + 100))
        if not self.__delay % 10:
            self.__gameload_index = (self.__gameload_index + 1) % 4

        # 定义开始游戏尺寸位置
        self.__gameStart_rect = self.gameStart.get_rect()
        self.__gameStart_rect.left = (WIDTH - self.__gameStart_rect.width) // 2
        self.__gameStart_rect.top = HEIGHT - 300

        self.__screen.blit(self.gameStart, self.__gameStart_rect)

        # 检测用户的鼠标操作
        if pygame.mouse.get_pressed()[0]:  # 用户按下鼠标左键
            # 获取鼠标位置
            self.__pos = pygame.mouse.get_pos()
            # 用户点击：重新开始
            if self.__gameStart_rect.left < self.__pos[0] < self.__gameStart_rect.right and self.__gameStart_rect.top < self.__pos[
                1] < self.__gameStart_rect.bottom:
                self.game_running = False

        self.__delay -= 1
        if self.__delay == 0:
            self.__delay = 100