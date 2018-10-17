import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """一个对自机发射子弹进行管理的类"""

    def __init__(self,ai_settings,screen,ship):
        """在自机所处位置创建一个子弹对象"""
        super().__init__()                  #继承Sprite类
        self.screen = screen

        #在(0,0)处创建一个表示子弹的矩形，再设置正确位置
        #pygame.Rect(矩形四角坐标)
        self.rect = pygame.Rect(0,0,ai_settings.bullet_width,
                                ai_settings.bullet_height)
        #设置正确位置
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        #存储用小数表示的子弹位置
        self.y = float(self.rect.y)

        self.color = ai_settings.bullet_color
        self.speed = ai_settings.bullet_speed


    def update(self):
        """向上移动子弹"""
        #更新表示子弹位置的小数值
        self.y -= self.speed
        #更新表示子弹的rect的位置
        self.rect.y = self.y

    def draw_bullet(self):
        """在屏幕上绘制子弹"""
        #pygame.draw.rect(画布，颜色，绘制内容)
        pygame.draw.rect(self.screen,self.color,self.rect)
