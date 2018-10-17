class Settings():
    """存储游戏所有设置的类"""

    def __init__(self):
        """初始化游戏静态设置"""
        #屏幕设置
        self.screen_width = 1000        #指定窗口尺寸
        self.screen_height = 650
        self.bg_color = (230,230,230)  #利用RGB值设置背景色
        
        #自机设置
        self.ship_limit = 3             #设置残机数
        
        #子弹设置
        self.bullet_width = 3           #设置子弹尺寸
        self.bullet_height = 15
        self.bullet_color = 60,60,60    #设置子弹颜色
        self.bullets_allowed = 3        #限制子弹数量

        #敌机设置
        self.fleet_drop_speed = 1       #设置敌机下落速度

        #以什么样的速度加快游戏节奏
        self.speedup_scale = 1.1

        self.initialize_dynamic_settings()


    def initialize_dynamic_settings(self):
        """初始化随游戏进行而变化的设置"""
        self.ship_speed = 5.5           #设置自机移动速度
        self.bullet_speed = 10          #设置子弹速度
        self.alien_speed = 1            #设置敌机速度

        self.fleet_direction = 1        #1表示右移，-1表示左移
        self.alien_points = 50           #计分：指定每个敌机的点数


    def increase_speed(self):
        """提高速度设置"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.alien_point = int(self.alien_points * self.score_scale)
        #print(self.alien_points)       #用于测试确认点数不断增加
