import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    """自机设置类"""

    def __init__(self,ai_settings,screen):
        """初始化自机并设置其初始位置"""
        super(Ship,self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        #加载自机图像并获取其“外接矩形”
        self.image = pygame.image.load('images/ship.bmp') #加载图像（点阵图）
        self.rect = self.image.get_rect()               #自机外接矩形函数
        self.screen_rect = screen.get_rect()            #屏幕外接矩形

        #将每个新自机放在屏幕底部中央，用外接矩形操作
        self.rect.centerx = self.screen_rect.centerx    #令自机中心x坐标=屏幕中心x坐标
        self.rect.bottom = self.screen_rect.bottom      #令自机底部=屏幕底部

        #在自机属性center中存储小数值
        self.center = float(self.rect.centerx)

        #移动标志
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """根据移动标志调整自机位置"""
        #更新自机center值，而不是rect
        #均使用if使二者响应优先级相同
        #并注意限制自机运动范围，以防滑出屏幕
        if self.moving_right and (self.rect.right < self.screen_rect.right):
            self.center += self.ai_settings.ship_speed
        if self.moving_left and (self.rect.left > 0):
            self.center -= self.ai_settings.ship_speed

        #根据self.center更新rect对象
        self.rect.centerx = self.center

    def blitme(self):
        """在指定位置绘制自机"""
        self.screen.blit(self.image,self.rect)  #根据self.rect指定的位置绘制self.image

    def center_ship(self):
        """让飞船在屏幕上居中"""
        self.center = self.screen_rect.centerx
