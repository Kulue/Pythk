import pygame
from pygame.sprite import Group                 #导入编组类
from settings import Settings                   #导入游戏设置类
from game_stats import GameStats                #导入游戏统计信息类
from scoreboard import Scoreboard               #导入记分牌
from button import Button                       #导入开始按钮
from ship import Ship                           #导入自机类
import game_functions as gf                      #导入运行模块并指定简称
    
def run_game():
    """初始化游戏并创建一个屏幕对象"""
    pygame.init()                                   #初始化背景设置
    ai_settings = Settings()                        #创建一个Settings实例
    screen = pygame.display.set_mode((ai_settings.screen_width,
                                     ai_settings.screen_height))
                                                    #指定尺寸
                                                    
    pygame.display.set_caption('glow')         #设置屏幕左上角显示标题

    #创建Play按钮
    play_button = Button(ai_settings,screen,"Play")

    #创建一个用于存储游戏统计信息的实例,并创建记分牌
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings,screen,stats)

    #创建自机实例
    ship = Ship(ai_settings,screen)
    
    #创建存储子弹的编组
    #导入pygame.sprite的Group类
    bullets = Group()
    #创建敌机编组
    aliens = Group()

    #创建敌机群
    gf.create_fleet(ai_settings,screen,ship,aliens)

    #开始游戏主循环
    #激活游戏动画循环后，每一次循环自动重绘屏幕(surface)
    while True:
        gf.check_events(ai_settings,screen,stats,sb,play_button,ship,aliens,
                        bullets)
        
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings,screen,stats,sb,ship,aliens,bullets)
            gf.update_aliens(ai_settings,screen,stats,sb,ship,aliens,bullets)
            
        gf.update_screen(ai_settings,screen,stats,sb,ship,aliens,bullets,
                         play_button)
        
run_game()                              #调用run_game()函数初始化并进入游戏
    
