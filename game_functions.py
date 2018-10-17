#用于存储控制游戏运行的函数

import sys                                      #退出时使用sys模块退出游戏
from time import sleep                          #用于暂停
import pygame
from bullet import Bullet                       #导入表示子弹的Bullet类
from alien import Alien                         #导入敌机类


def check_keydown_events(event,ai_settings,screen,ship,bullets):
    """响应按键"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings,screen,ship,bullets)
    elif event.key == pygame.K_q:
        sys.exit()                              #按Q键可退出游戏
        
def check_keyup_events(event,ship):
    """响应松开"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
        
def check_events(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets):
    """响应按键和鼠标事件"""
     #监视键盘及鼠标事件（事件循环）
    for event in pygame.event.get():
        if event.type == pygame.QUIT:           #点击屏幕关闭按钮
            sys.exit()                          #sys模块退出函数
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event,ai_settings,screen,ship,bullets)       
        elif event.type == pygame.KEYUP:
            check_keyup_events(event,ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings,screen,stats,sb,play_button,
                              ship,aliens,bullets,mouse_x,mouse_y)
            
def check_play_button(ai_settings,screen,stats,sb,play_button,ship,aliens,
                      bullets,mouse_x,mouse_y):
    """在玩家单机Play按钮时开始新游戏"""
    #collidepoint检查鼠标点击处是否在play按钮范围内
    button_clicked = play_button.rect.collidepoint(mouse_x,mouse_y)
    if button_clicked and not stats.game_active:    #游戏非活动时点击play区域才有用
        #重置游戏设置
        ai_settings.initialize_dynamic_settings()
        #隐藏光标
        pygame.mouse.set_visible(False)
        #重置游戏统计信息
        stats.reset_stats()
        stats.game_active = True
        #重置记分牌图像
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()
        #清空敌机和子弹列表
        aliens.empty()
        bullets.empty()
        #创建新敌机群，并让自机居中
        create_fleet(ai_settings,screen,ship,aliens)
        ship.center_ship()



def update_screen(ai_settings,screen,stats,sb,ship,aliens,bullets,play_button):
    """更新屏幕上的图像，并切换到新屏幕"""
    #每次循环重新填充背景色并重新放置自机
    screen.fill(ai_settings.bg_color)
    #重绘所有子弹
    for bullet in bullets.sprites():            #方法bullets.sprites()返回一个列表
        bullet.draw_bullet()
    #绘制自机和敌机
    ship.blitme()
    aliens.draw(screen)                         #绘制敌机编组中每个元素

    #显示得分
    sb.show_score()

    #如果游戏处于非活动状态，就绘制Play按钮
    if not stats.game_active:
        play_button.draw_button()

    #让最近绘制的屏幕可见
    pygame.display.flip()                       #擦去旧屏幕，显示新屏幕

def update_bullets(ai_settings,screen,stats,sb,ship,aliens,bullets):
    """更新子弹位置，并删除已消失子弹"""
    #更新子弹位置
    bullets.update()
    
    #删除已消失子弹
    #不应从列表或编组条目中删除，应当遍历编组的副本
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collisions(ai_settings,screen,stats,sb,ship,aliens,
                                  bullets)
    
def check_bullet_alien_collisions(ai_settings,screen,stats,sb,ship,aliens,
                                  bullets):
    """检查是否有子弹击中敌机，若有则删除相应子弹和敌机"""
    #遍历子弹和敌机编组，有重叠则建立二者键（子弹）值（敌机）对
    collisions = pygame.sprite.groupcollide(bullets,aliens,True,True)

    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats,sb)
    
    if len(aliens) == 0:
        #删除现有子弹并新建一群敌机
        bullets.empty()
        ai_settings.increase_speed()

        #提高等级
        stats.level += 1
        sb.prep_level()
        
        create_fleet(ai_settings,screen,ship,aliens)
        
def fire_bullet(ai_settings,screen,ship,bullets):
    #创建一颗子弹并将其加入到bullets编组中（发射子弹）
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings,screen,ship)
        bullets.add(new_bullet)


def get_numbers_aliens_x(ai_settings,alien_width):
    """计算每行可容纳敌机数"""
    available_space_x  = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def get_number_rows(ai_settings,ship_height,alien_height):
    """计算屏幕可容纳敌机行数"""
    available_space_y = (ai_settings.screen_height
                         - (3 * alien_height)
                         - (3 * ship_height))
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows



def create_alien(ai_settings,screen,aliens,alien_number,row_number):
    """创建一个敌机并将其放在当前行"""
    alien = Alien(ai_settings,screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)

def create_fleet(ai_settings,screen,ship,aliens):
    """创建敌机群"""
    #创建一个敌机并计算一行可容纳多少敌机
    #敌机间距为敌机宽度
    alien = Alien(ai_settings,screen)           #创建敌机实例
    number_aliens_x = get_numbers_aliens_x(ai_settings,alien.rect.width)
    number_rows = get_number_rows(ai_settings,ship.rect.height,alien.rect.height)
    
    #创建敌机群
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings,screen,aliens,alien_number,row_number)

            

def check_fleet_edges(ai_settings,aliens):
    """有敌机到达边缘时采取相应措施"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings,aliens)

def change_fleet_direction(ai_settings,aliens):
    """将敌机群下移并改变左右方向"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def ship_hit(ai_settings,screen,stats,sb,ship,aliens,bullets):
    """响应敌机与自机相撞"""
    if stats.ships_left > 0:
        #将残机数ships_left减一
        stats.ships_left -= 1
        #更新记分牌
        sb.prep_ships()

        #清空敌机和子弹列表
        aliens.empty()
        bullets.empty()

        #创建一群新敌机，并将自机放到屏幕底端中央
        create_fleet(ai_settings,screen,ship,aliens)
        ship.center_ship()

        #暂停
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)  #重新显示光标

def check_aliens_bottom(ai_settings,screen,stats,sb,ship,aliens,bullets):
    """检查是否有敌机触底"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            #像自机被撞到一样处理
            ship_hit(ai_settings,screen,stats,sb,ship,aliens,bullets)
            break

def update_aliens(ai_settings,screen,stats,sb,ship,aliens,bullets):
    """
    检查是否有敌机到达屏幕边缘，然后更新所有敌机位置
    """
    check_fleet_edges(ai_settings,aliens)
    aliens.update()

    #检测自机与敌机之间的碰撞
    if pygame.sprite.spritecollideany(ship,aliens):
        ship_hit(ai_settings,screen,stats,sb,ship,aliens,bullets)

    #检查是否有敌机触底
    check_aliens_bottom(ai_settings,screen,stats,sb,ship,aliens,bullets)



def check_high_score(stats,sb):
    """在屏幕上显示当前得分和最高得分"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()
