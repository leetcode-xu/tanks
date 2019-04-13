import sys
import threading
import time

from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton

from Bullet import bullet
from Global import quan_var
from Worker import work_bullet

# 我方坦克类
class mytank:
    def __init__(self,x, y, tank_two=None):
        self.flag = 5     #  我方坦克的标志数字
        self.x = x        #  初始位置坐标x值，单位像素
        self.y = y        #  初始位置坐标y值，单位像素
        self.fangxiang = (0, -1)    #  初始化坦克方向，向上
        self.tank_two = tank_two    #  坦克二号玩家标志位
        self.life = quan_var.mytank_life       #  初始化塔坦克生命值
        self.lock = threading.Lock()           #  初始化线程锁
        self.bullet_type = 1         #  子弹类型
    def tank_qiehuan(self, fangxiang = None):
        if fangxiang == None:
            # 坦克玩家一
            if not self.tank_two:
                #  print('wanjiaer',self)
                self.tank_player.setStyleSheet('QPushButton{border-image:url(./image/myTank/tank_up.png);}')
            # 坦克玩家二
            else:
                #  print('wanjiayi',self)
                self.tank_player.setStyleSheet('QPushButton{border-image:url(./image/myTank/tank_two_up.png);}')
        else:
            #  坦克玩家一
            if not self.tank_two:
                self.tank_player.setStyleSheet('QPushButton{border-image:url(./image/myTank/tank_%s.png);}'%fangxiang)
            # 坦克玩家二
            else:
                self.tank_player.setStyleSheet('QPushButton{border-image:url(./image/myTank/tank_two_%s.png);}'%fangxiang)

    def chusheng(self, frame):# 18*26
        self.frame = frame
        # 玩家控件
        self.tank_player = QPushButton(frame)
        #  设置位置大小
        self.tank_player.setGeometry(self.x, self.y, 48, 48)
        #  self.tank_player.setGeometry(18*24, 26*24, 48, 48)
        # 根据是玩家一还是玩家二，显示相应的颜色
        self.tank_qiehuan()
        # 将坦克位置信息同步到全局变量中
        self.gengxin_map_dict(self.x//24, self.y//24)
        #  根据像素点 存放我方坦克对象
        self.flag_mytank()

    def gengxin_map_dict(self, x, y):  # 更新map_dict中的我方坦克位置
        #  给修改操作加锁，避免高并发出错
        self.lock.acquire(timeout=0.02)
        x-=1
        y-=1
        quan_var.map_dict[(x, y)] = self.flag
        quan_var.map_dict[(x + 1, y)] = self.flag
        quan_var.map_dict[(x, y + 1)] = self.flag
        quan_var.map_dict[(x + 1, y + 1)] = self.flag
        # 释放锁
        self.lock.release()
    # 更新mytank_dict字典中的我方坦克信息
    def flag_mytank(self):
        self.lock.acquire(timeout=0.02)
        for key, value in quan_var.mytank_dict.copy().items():
            if value==self:
                del quan_var.mytank_dict[key]
        quan_var.mytank_dict[(self.x, self.y)] = self
        self.lock.release()
    def fashe(self): # 发射子弹
        #  一个子弹线程没有结束，不允许发射子弹
        if not quan_var.thread_life:
            quan_var.thread_life = True
            self.bu = bullet(self.frame, self, self.tank_player)
            try:
                # 实例化我方子弹工作类
                self.work = work_bullet(self.bu)
                # 线程初始化
                self.thread = QThread()
                # 将子弹工作类对象添加到线程中
                self.work.moveToThread(self.thread)
                # 将fa_bullet_singnal信号绑定子弹移动方法
                self.work.fa_bullet_singnal.connect(self.bu.move)
                # 将线程结束信号绑定线程退出方法
                self.work.jieshu1.connect(lambda: self.thread.quit())
                # 将线程被启动信号绑定fa_bullet方法
                self.thread.started.connect(self.work.fa_bullet)
                # 启动线程
                self.thread.start()
                print(self.bullet_type,'zidanleixing')
            except Exception as e:
                print(e,'发射子弹错误')
    def get_life(self):
        if quan_var.life_list.get(self, 0):
            # 在辅界面中显示坦克的生命值
            quan_var.life_list[self].setText('%s'%self.life)
    # 预留‘接口’函数，子弹判断击中我方坦克，即调用它
    def siwang(self):#  死亡
        # 把标志位设为零
        self.flag = 0
        self.gengxin_map_dict(self.x//24, self.y//24)  # 清除死亡位置足迹
        self.bullet_type = 1  #  将子弹类型置为 1
        #  生命值大于一，即生命值减一
        if self.life>1:
            self.life-=1
            #  可添加被击中效果
            #  对玩家一的操作
            if not self.tank_two:
                self.tank_player.setGeometry(17*24, 25*24, 48, 48)  # 玩家一回到初始位置
                self.x, self.y = 17*24, 25*24
            #  对玩家二的操作
            else:
                self.tank_player.setGeometry(9 * 24, 25 * 24, 48, 48)  #  玩家二回到初始位置
                self.x, self.y = 9 * 24, 25 * 24
            #  设置标记位为5
            self.flag = 5
            self.gengxin_map_dict(self.x//24, self.y//24) # 更新出生位置
            self.flag_mytank()  #  更新我方坦克 位置对象 字典
            self.get_life()
        #  生命值为一被击中的时候，清除坦克
        else:
            del quan_var.mytank_dict[(self.x, self.y)]
            self.tank_player.setVisible(False)
            self.flag = 0
            self.get_life()
        #  我方坦克全部死亡，游戏结束，判输
        if not quan_var.mytank_dict:
            self.gameover = QLabel(quan_var.frame_one)
            self.gameover.setGeometry(86, 172, 497, 249)
            self.gameover.setStyleSheet('QLabel{border-image:url(./image/home/timg.png)}')
            self.gameover.setWindowOpacity(0.4)
            self.gameover.setVisible(True)
            QApplication.processEvents()
            quan_var.defeat.play()
            time.sleep(1.2)
            print('jie shu you xi')
            #  sys.exit(QApplication(sys.argv).exec_())
            sys.exit(0)
    #  坦克移动函数
    def move(self, fangxiang):  #  移动  根据方向键定移动方向  frame为坦克所处界面对象
        #  设置运动方向
        self.fangxiang = fangxiang
        qian_flag = self.is_qian()
        print('qianfang',qian_flag)
        #  如果可向前运动
        if max(qian_flag) <= 1:
            if max(qian_flag) == 0.1:  #  手雷
                quan_var.add_food.play()
                quan_var.food_obj.siwang()
                mytank_obj_list = list(quan_var.mytank_dict.values())
                for enytank in quan_var.life_list:
                    if enytank not in mytank_obj_list:
                        print('调用敌方坦克siwang')
                        enytank.siwang()
            elif max(qian_flag) == 0.2:  #  五角星
                quan_var.food_obj.siwang()
                quan_var.add_food.play()
                self.bullet_type += 1
                quan_var.bullet_type_dict[self] = self.bullet_type
            elif max(qian_flag) == 0.3:  #  生命值
                quan_var.add_food.play()
                quan_var.food_obj.siwang()
                self.life += 1
                quan_var.mytank_life = self.life
                self.get_life()
            else:
                pass
            self.flag = 0
            self.gengxin_map_dict(self.x//24, self.y//24)  #  清除之前map_dict上mytank的位置
            #  运动之后的坐标（单位像素）
            self.x = self.x+self.fangxiang[0]*quan_var.mytank_speed
            self.y += self.fangxiang[1]*quan_var.mytank_speed
            if quan_var.food_dict.get((self.x, self.y), 0):
                quan_var.food_dict.get((self.x, self.y), 0).siwang()
            #  改变其对应位置
            self.tank_player.setGeometry(self.x, self.y, 48,48)
            #  self.changSudu()
            self.flag = 5
            self.gengxin_map_dict(self.x//24, self.y//24)  #  更新map_dict   玩家一位置
            #  更新quan_var.mytank_dict列表
            self.flag_mytank()
    #  判断坦克能否往前  返回类型（标志数，标志数） 告诉move方法 坦克前面是什么
    def is_qian(self):
        x,y = self.x, self.y
        if self.fangxiang==(1, 0):#  #  方向为右
                   # 右上                                                    右下
            # 根据玩家信息，显示相应的颜色
            self.tank_qiehuan('right')
            return quan_var.map_dict.get((x // 24 + 1 , y // 24 - 1), 0), quan_var.map_dict.get((x // 24 + 1  , y // 24 ), 0)
        elif self.fangxiang==(-1, 0): #  方向为左
            #  左上                                                                                左下
            self.tank_qiehuan('left')
            return quan_var.map_dict.get(((x-quan_var.mytank_speed) // 24 - 1, y // 24 - 1), 0), quan_var.map_dict.get(((x-quan_var.mytank_speed) // 24 - 1, y // 24), 0)
        elif self.fangxiang==(0, 1): # 方向为下
            #  左下                                                          右下
            self.tank_qiehuan('down')
            return quan_var.map_dict.get((x // 24 - 1, y // 24 + 1), 0), quan_var.map_dict.get((x // 24, y // 24 + 1), 0)
        else :  # 方向为上
            #  左上                                                                               右上
            self.tank_qiehuan('up')
            return quan_var.map_dict.get((x // 24 - 1, (y - quan_var.mytank_speed) // 24 - 1), 0), quan_var.map_dict.get((x // 24, (y - quan_var.mytank_speed) // 24 - 1), 0)
    #  改变坦克速度函数，未被调用
    def changSudu(self):
        for i in range(1, 5):
            self.x = self.x + self.fangxiang[0] * quan_var.mytank_speed//4
            self.y += self.fangxiang[1] * quan_var.mytank_speed//4
            self.tank_player.setGeometry(self.x, self.y, 48, 48)
            time.sleep(0.05)
