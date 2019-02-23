import time
import sys
from PyQt5.QtWidgets import QLabel, QApplication, QPushButton

from Global import quan_var

#子弹模块
class bullet:
    def __init__(self, frame, obj_tan, tank_player):
        self.obj_tan = obj_tan               # 发送子弹的坦克对象
        self.fangxiang = obj_tan.fangxiang   # 坦克方向
        self.obj_tan_button = tank_player    # 坦克中的图标对象
        self.frame = frame                   # 画板对象  第二级画板 frame_two
        self.life = True                     # 子弹生命值
        self.speed = 12                      # 子弹速度  单位像素
        self.xy_()                           # 初始化子弹的初始位置

#根据坦克坐标初始化子弹坐标
    def xy_(self):
        x = self.obj_tan_button.x()
        y = self.obj_tan_button.y()
        if self.fangxiang == (0, -1):
            # 子弹往上显示
            self.x = x+18
            self.y = y-12
        elif self.fangxiang == (0, 1):
            #子弹向下显示
            self.x = x + 18
            self.y = y + 48
        elif self.fangxiang == (-1, 0):
            # 子弹像左显示
            self.x = x - 12
            self.y = y + 18
        else :
            # 子弹向右显示
            self.x = x + 48
            self.y = y + 18
        #根据子弹的坐标显示其图像
        self.show()

    #子弹移动一个基本单位长度
    def move(self):
        #得到子弹前方的物体类型
        is_tuple = self.is_qian()
        print('is_tuple:',is_tuple)
        # 如果前方有钢墙或边框的存在，处理如下
        if 1==self.obj_tan.bullet_type and (3 in is_tuple[0]) or 10 in is_tuple[0]:
            try:
                # pygame.mixer.music.stop()
                quan_var.bang_sound.play()
                self.siwang()
            except Exception as e:
                pass
        # 捡到五角星后的子弹
        elif self.obj_tan.bullet_type >= 2 and 3 in is_tuple[0]:
            try:
                is_tuple_one = (is_tuple[1][0] - 24) // 24, (is_tuple[1][1] - 24) // 24
                is_tuple_two = (is_tuple[2][0] - 24) // 24, (is_tuple[2][1] - 24) // 24
                quan_var.map_dict[is_tuple_one] = 0
                quan_var.map_dict[is_tuple_two] = 0
                # quan_var.static_obj[(is_tuple_one[0] * 24 + 24, is_tuple_one[1] * 24 + 24)].setVisible(False)
                # quan_var.static_obj[(is_tuple_two[0] * 24 + 24, is_tuple_two[1] * 24 + 24)].setVisible(False)
                if quan_var.static_obj.get(((is_tuple_one[0] * 24 + 24, is_tuple_one[1] * 24 + 24)), 0):
                    quan_var.static_obj[(is_tuple_one[0] * 24 + 24, is_tuple_one[1] * 24 + 24)].setVisible(False)
                if quan_var.static_obj.get(((is_tuple_two[0] * 24 + 24, is_tuple_two[1] * 24 + 24)), 0):
                    quan_var.static_obj[(is_tuple_two[0] * 24 + 24, is_tuple_two[1] * 24 + 24)].setVisible(False)
                quan_var.bang_sound.play()
                self.siwang()
            except Exception as e:
                print('击中钢墙错误, 子弹类型二', e)
        # 如果老鹰被击中，游戏结束，为输
        elif is_tuple[0] == (4, 4):
            quan_var.bang_sound.play()
            quan_var.defeat.play()
            self.siwang()
            quan_var.laoying.setVisible(False)
            self.gamevoer = QLabel(quan_var.frame_one)
            self.gamevoer.setGeometry(66, 162, 540, 270)
            self.gamevoer.setStyleSheet('QLabel{border-image:url(./image/home/timg.png)}')
            # self.gamevoer.setWindowOpacity(0.4)
            self.gamevoer.setVisible(True)
            QApplication.processEvents()
            time.sleep(1.2)
            sys.exit(0)
        #我方坦克被击中的处理方式
        elif is_tuple[0] == (5, 5):
            #如果被敌方坦克击中处理，被我方坦克击中不处理。
            if self.obj_tan not in list(quan_var.mytank_dict.values()):
                try:
                    #取出坦克被击中时的坐标，
                    is_tuple_one = is_tuple[1][0] // 24 * 24, is_tuple[1][1] // 24 * 24
                    #根据坐标，取出我方坦克对象。 调用它自身的死亡函数
                    quan_var.mytank_dict[is_tuple_one].siwang()
                except Exception as e:
                    print('我方坦克被击中出错',e)
            quan_var.bang_sound.play()
            self.siwang()
        #如果敌方坦克被击中
        elif is_tuple[0] == (6, 6):
            # 如果子弹不是敌方坦克发出的，做以下处理，敌方坦克发出的不作处理
            if self.obj_tan not in [i for i in quan_var.enytank_dict.values()]:
                try :
                    #同理取出被击中坦克坐标
                    is_tuple_one = is_tuple[1][0] // 24*24, is_tuple[1][1] // 24*24
                    print("self.is_qian()",self.is_qian())
                    #根据坐标取出敌方坦克对象，并调用他自身的死亡函数
                    quan_var.enytank_dict[is_tuple_one].siwang()
                    if quan_var.enytank_dict.get(is_tuple_one, 0):
                        quan_var.enytank_dict[is_tuple_one].siwang()
                    quan_var.bang_sound.play()
                except Exception as e:
                    print('敌方坦克被击中出错',e)
            self.siwang()
        #如果前方是土砖、土砖
        elif is_tuple[0] == (2, 2):
            try:
                #取出子弹左前方土砖坐标
                is_tuple_one = (is_tuple[1][0] - 24)//24, (is_tuple[1][1] - 24)//24
                #取出子弹右前方土砖坐标
                is_tuple_two =(is_tuple[2][0] - 24)//24, (is_tuple[2][1]-24)//24
                quan_var.map_dict[is_tuple_one] = 0
                quan_var.map_dict[is_tuple_two] = 0
                #同理根据坐标获取其对象，将其设置为不显示
                quan_var.static_obj[(is_tuple_one[0]*24+24,is_tuple_one[1]*24+24)].setVisible(False)
                quan_var.static_obj[(is_tuple_two[0]*24+24,is_tuple_two[1]*24+24)].setVisible(False)
                quan_var.bang_sound.play()
                self.siwang()
            except Exception as e:
                print('击中土砖错误',e)
        #如果前方是 空气，土砖
        elif is_tuple[0] == (0, 2):
            try:
                is_tuple_one = (is_tuple[1][0] - 24)//24, (is_tuple[1][1] - 24)//24
                is_tuple_two =(is_tuple[2][0] - 24)//24, (is_tuple[2][1]-24)//24
                quan_var.map_dict[is_tuple_one] = 0
                quan_var.map_dict[is_tuple_two] = 0
                # quan_var.static_obj[(is_tuple_one[0]*24+24,is_tuple_one[1]*24+24)].setVisible(False)
                quan_var.static_obj[(is_tuple_two[0]*24+24,is_tuple_two[1]*24+24)].setVisible(False)
                quan_var.bang_sound.play()
                self.siwang()
            except Exception as e:
                print('击中土砖错误',e)
        #如果前方是 土砖，空气
        elif is_tuple[0] == (2, 0):
            try:
                is_tuple_one = (is_tuple[1][0] - 24)//24, (is_tuple[1][1] - 24)//24
                is_tuple_two =(is_tuple[2][0] - 24)//24, (is_tuple[2][1]-24)//24
                quan_var.map_dict[is_tuple_one] = 0
                quan_var.map_dict[is_tuple_two] = 0
                quan_var.static_obj[(is_tuple_one[0]*24+24,is_tuple_one[1]*24+24)].setVisible(False)
                # quan_var.static_obj[(is_tuple_two[0]*24+24,is_tuple_two[1]*24+24)].setVisible(False)
                quan_var.bang_sound.play()
                self.siwang()
            except Exception as e:
                print('击中土砖错误',e)
        #如果前方是土砖，老鹰
        elif is_tuple[0] == (2, 4):
            try:
                is_tuple_one = (is_tuple[1][0] - 24)//24, (is_tuple[1][1] - 24)//24
                is_tuple_two =(is_tuple[2][0] - 24)//24, (is_tuple[2][1]-24)//24
                quan_var.map_dict[is_tuple_one] = 0
                # quan_var.map_dict[is_tuple_two] = 0
                quan_var.static_obj[(is_tuple_one[0]*24+24,is_tuple_one[1]*24+24)].setVisible(False)
                # quan_var.static_obj[(is_tuple_two[0]*24+24,is_tuple_two[1]*24+24)].setVisible(False)
                quan_var.bang_sound.play()
                self.siwang()
            except Exception as e:
                print('击中土砖错误',e)
        #如果前方是老鹰，土砖
        elif is_tuple[0] == (4, 2):
            try:
                is_tuple_one = (is_tuple[1][0] - 24)//24, (is_tuple[1][1] - 24)//24
                is_tuple_two =(is_tuple[2][0] - 24)//24, (is_tuple[2][1]-24)//24
                # quan_var.map_dict[is_tuple_one] = 0
                quan_var.map_dict[is_tuple_two] = 0
                # quan_var.static_obj[(is_tuple_one[0]*24+24,is_tuple_one[1]*24+24)].setVisible(False)
                quan_var.static_obj[(is_tuple_two[0]*24+24,is_tuple_two[1]*24+24)].setVisible(False)
                quan_var.bang_sound.play()
                self.siwang()
            except Exception as e:
                print('击中土砖错误',e)
        # 如果前方是土砖，树木
        elif is_tuple[0] == (2, 1):
            try:
                is_tuple_one = (is_tuple[1][0] - 24)//24, (is_tuple[1][1] - 24)//24
                is_tuple_two =(is_tuple[2][0] - 24)//24, (is_tuple[2][1]-24)//24
                quan_var.map_dict[is_tuple_one] = 0
                # quan_var.map_dict[is_tuple_two] = 0
                quan_var.static_obj[(is_tuple_one[0]*24+24,is_tuple_one[1]*24+24)].setVisible(False)
                # quan_var.static_obj[(is_tuple_two[0]*24+24,is_tuple_two[1]*24+24)].setVisible(False)
                quan_var.bang_sound.play()
                self.siwang()
            except Exception as e:
                print('击中土砖错误',e)
        # 如果前方是 树木，土砖
        elif is_tuple[0] == (1, 2):
            try:
                is_tuple_one = (is_tuple[1][0] - 24)//24, (is_tuple[1][1] - 24)//24
                is_tuple_two =(is_tuple[2][0] - 24)//24, (is_tuple[2][1]-24)//24
                # quan_var.map_dict[is_tuple_one] = 0
                quan_var.map_dict[is_tuple_two] = 0
                # quan_var.static_obj[(is_tuple_one[0]*24+24,is_tuple_one[1]*24+24)].setVisible(False)
                quan_var.static_obj[(is_tuple_two[0]*24+24,is_tuple_two[1]*24+24)].setVisible(False)
                quan_var.bang_sound.play()
                self.siwang()
            except Exception as e:
                print('击中土砖错误',e)
        # 除以上可能之外
        else:
            self.x = self.x + self.speed*self.fangxiang[0]
            self.y = self.y + self.speed*self.fangxiang[1]
            self.bullet_.setGeometry(self.x, self.y, 12, 12)
            self.bullet_.setVisible(True)
    # 返回子弹前方物品类型  retype：（（左前方类型，右前方类型），（左前方物品像素坐标），（右前方物品像素坐标））
    def is_qian(self):
        # 判断子弹在前进的过程中会遇到什么
        if self.fangxiang == (0, 1): #down
            return (quan_var.map_dict.get(((self.x-18-24)//24, (self.y+self.speed-24)//24), 0), quan_var.map_dict.get(((self.x+6-24)//24, (self.y + self.speed-24)//24),0)),\
                   (self.x-18, self.y+self.speed), (self.x+6, self.y + self.speed)
        elif self.fangxiang ==(0, -1): #up
            return (quan_var.map_dict.get(((self.x-42)//24, (self.y - self.speed-24)//24), 0), quan_var.map_dict.get(((self.x -18)//24, (self.y -self.speed-24)//24),0)),\
                   (self.x-18, self.y -self.speed), (self.x +6, self.y -self.speed)
        elif self.fangxiang == (1, 0): # right
            return (quan_var.map_dict.get(((self.x +self.speed-24)//24, (self.y -18-24)//24), 0), quan_var.map_dict.get(((self.x +self.speed-24)//24, (self.y+6-24)//24),0)),\
                   (self.x +self.speed, self.y -18), (self.x +self.speed, self.y+6)
        elif self.fangxiang ==(-1, 0): #left
            return (quan_var.map_dict.get(((self.x-self.speed-24)//24,(self.y-18-24)//24),0), quan_var.map_dict.get(((self.x-self.speed-24)//24,(self.y+6-24)//24),0)),\
                   (self.x-self.speed,self.y-18), (self.x-self.speed,self.y+6)
    #子弹的死亡函数，添加爆炸效果，并消失
    def siwang(self):
        self.bullet_.setGeometry(self.x - 18, self.y - 18, 48, 48)
        self.bullet_.setStyleSheet('QPushButton{border-image:url(./image/others/boom_static.png)}')
        QApplication.processEvents()
        time.sleep(0.025)
        self.life = False
        self.bullet_.setVisible(False)

    #根据子弹坐标显示子弹
    def show(self):
        fangxiang_dicts = {(-1,0):'left',(1,0):'right', (0, -1):'up', (0,1):'down'}
        self.bullet_ = QPushButton(self.frame)
        self.bullet_.setGeometry(self.x, self.y, 12, 12)
        self.bullet_.setStyleSheet('QPushButton{border-image:url(./image/bullet/bullet_%s.png)}'%fangxiang_dicts[self.fangxiang])
        self.bullet_.setVisible(True)
