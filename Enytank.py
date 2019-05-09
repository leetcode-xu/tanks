import random
import sys
import threading
import time

from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QLabel, QApplication, QPushButton

from Bullet import bullet
from Global import quan_var
from Worker import work_bullet


# 敌方坦克类
class enytank:

    def __init__(self, frame):
        self.frame = frame               # 存在的画板
        self.eny_bullet_life = True      # 坦克生命标记位
        self.life =3                     # 生命值
        self.fangxiang = (0,1)           # 方向
        self.lock = threading.Lock()     # 初始化锁对象
        self.bullet_type = 1             # 子弹类型
        self.bullet_list = []            # 子弹列表，作用：不允许同一个坦克在一个子弹运动未结束之前发射子弹（性能的限制，欢迎各位改进）
        self.set_xy()                    # 根据四个可选位置随机生成一个坦克

    def set_xy(self):
        # 根据四个可选位置随机生成一个坦克
        while True:
            self.x, self.y = random.choice(((24, 24),(8*24, 24),(15*24, 24),(25*24, 24)))
            # 没有可选位置时，结束循环
            if self.tank_true():
                break
    # 坦克出生之前，判断位置该位置是否被占用

    def tank_true(self):
        if quan_var.map_dict.get((self.x//24, self.y//24), 0)>1:
            return False
        elif quan_var.map_dict.get((self.x//24, self.y//24-1), 0)>1:
            return False
        elif quan_var.map_dict.get((self.x//24-1, self.y//24), 0)>1:
            return False
        elif quan_var.map_dict.get((self.x//24-1, self.y//24-1), 0)>1:
            return False
        else:
            self.gengxin_map_dict()
            self.genxin_enytank_dict()
            return True
    # 更新敌方坦克位置信息到quan_var.map_dict字典中

    def gengxin_map_dict(self, flag = 6):
        self.lock.acquire(timeout=0.02)
        quan_var.map_dict[self.x//24-1, self.y//24-1] = flag
        quan_var.map_dict[self.x//24, self.y//24-1] = flag
        quan_var.map_dict[self.x//24-1, self.y//24] = flag
        quan_var.map_dict[self.x//24, self.y//24] = flag
        self.lock.release()

    # 更新gengxin_enytank_dict字典信息
    def genxin_enytank_dict(self):
        self.lock.acquire(timeout=0.02)
        for key, value in quan_var.enytank_dict.copy().items():
            if value ==self:
                del quan_var.enytank_dict[key]
        quan_var.enytank_dict[(self.x, self.y)] = self
        quan_var.enytank_dict[(self.x + 24, self.y)] = self
        quan_var.enytank_dict[(self.x, self.y + 24)] = self
        quan_var.enytank_dict[(self.x + 24, self.y + 24)] = self
        self.lock.release()

    # 生成敌方坦克
    def chusheng(self):
        # 界面敌方坦克数量加一
        quan_var.now_enytank_num +=1
        # 敌方坦克总数量减一
        quan_var.enytank_num -=1
        # 随机生成坦克的生命值
        self.life = random.randint(1, 3)
        # 在辅界面中显示其生命值
        self.get_life()
        # 显示敌方坦克剩余数量
        quan_var.main_obj.label_9.setText("%s"%(quan_var.enytank_num+quan_var.now_enytank_num))
        image_url = './image/enemyTank/enemy_%s_down.png'%str(self.life)
        self.enytank_button = QPushButton(self.frame)
        self.enytank_button.setText('')
        self.enytank_button.setGeometry(self.x, self.y, 48, 48)
        # 根据生命值显示其对应的颜色
        self.enytank_button.setStyleSheet('QPushButton{border-image:url(%s)}'%image_url)
        self.enytank_button.setVisible(True)

    # 在敌方坦克死亡一个的时候再出生一个，共用self.enytank_button对象，
    def again_chusheng(self):
        quan_var.now_enytank_num += 1
        quan_var.enytank_num -= 1
        self.life = random.randint(1, 3)
        self.get_life()
        quan_var.main_obj.label_9.setText("%s" % (quan_var.enytank_num + quan_var.now_enytank_num))
        image_url = './image/enemyTank/enemy_%s_down.png' % str(self.life)
        self.enytank_button.setGeometry(self.x, self.y, 48, 48)
        self.enytank_button.setStyleSheet('QPushButton{border-image:url(%s)}' % image_url)
        self.enytank_button.setVisible(True)

    # 坦克移动
    def move(self):
        # 获取前方物品状态
        self.qianfang = self.is_qian()
        # 可往前运动，即做如下操作
        if max(self.qianfang)<2:
            self.enytank_button.setGeometry(self.x +self.fangxiang[0]*24, self.y + self.fangxiang[1]*24, 48, 48)
            self.gengxin_map_dict(0)
            self.x = self.x+self.fangxiang[0]*24
            self.y = self.y+self.fangxiang[1]*24
            # if random.randint(1,2) == 1:
            # 发射子弹
            self.fashe()
            self.gengxin_map_dict()
            self.genxin_enytank_dict()

    def set_bullet_life(self):
        self.thread.quit()
        # 上一个子弹线程退出，将eny_bullet_life标志位变为True
        self.eny_bullet_life = True

    # 发射子弹函数
    def fashe(self):
        # 只有上一个子弹线程完全退出了，才允许发射下一发子弹，（由于本人技术限制）
        if self.eny_bullet_life:
            try:
                self.eny_bullet_life = False
                self.eny_bullet = bullet(self.frame, self, self.enytank_button)
                self.work = work_bullet(self.eny_bullet)
                self.thread = QThread()
                self.work.fa_bullet_eny.connect(self.eny_bullet.move)
                self.work.moveToThread(self.thread)
                self.work.jieshu.connect(self.set_bullet_life)
                self.thread.started.connect(self.work.fa_bullet_enytank)
                self.thread.start()
            except Exception as e:
                pass

    # 返回前方物体类型  ，返回值类型：（标志数，标志数）
    def is_qian(self):
        # 随机生成一个方向，其中向下概率37.5%   向左向右 25%    向上12.5%
        self.fangxiang = random.choice(((0, -1),(0, 1),(0, 1),(0, 1),(-1, 0),(1, 0),(-1, 0),(1, 0)))
        if self.fangxiang==(1, 0):  # 方向为右
            # 右上                                                    右下
            self.enytank_button.setStyleSheet('QPushButton{border-image:url(./image/enemyTank/enemy_%s_right.png);}'% str(self.life))
            return quan_var.map_dict.get((self.x // 24 + 1 , self.y // 24 - 1), 0), quan_var.map_dict.get((self.x // 24 + 1  , self.y // 24 ), 0)
        elif self.fangxiang==(-1, 0): # 方向为左
            # 左上                                                     左下
            self.enytank_button.setStyleSheet('QPushButton{border-image:url(./image/enemyTank/enemy_%s_left.png);}'% str(self.life))
            return quan_var.map_dict.get(((self.x-24) // 24 - 1, self.y // 24 - 1), 0), quan_var.map_dict.get(((self.x-24) // 24 - 1, self.y // 24), 0)
        elif self.fangxiang==(0, 1): #方向为下
            # 左下                                                     右下
            self.enytank_button.setStyleSheet('QPushButton{border-image:url(./image/enemyTank/enemy_%s_down.png);}'% str(self.life))
            return quan_var.map_dict.get((self.x // 24 - 1, self.y // 24 + 1), 0), quan_var.map_dict.get((self.x // 24, self.y // 24 + 1), 0)
        else:  # 方向为上
            # 左上                                                     右上
            self.enytank_button.setStyleSheet('QPushButton{border-image:url(./image/enemyTank/enemy_%s_up.png);}'% str(self.life))
            return quan_var.map_dict.get((self.x // 24 - 1, (self.y - 24) // 24 - 1), 0), quan_var.map_dict.get((self.x // 24, (self.y - 24) // 24 - 1), 0)

    def get_life(self):
        if quan_var.life_list.get(self, 0):
            # 在辅界面上显示其生命值
            quan_var.life_list.get(self, 0).setText('%s'%self.life)

    # 预留“接口”函数供子弹类调用，子弹判断击中，即调用
    def siwang(self):
        # 增加分数
        quan_var.fenshu +=100
        # 在辅界面上显示分数
        quan_var.main_obj.game_zhi.setText('%s'%quan_var.fenshu)
        # 当生命值大于一的时候，只做减一操作
        if self.life > 1 :
            self.life -= 1
            self.get_life()
            print('坦克被击中 生命值减一 换相应的颜色')
        # 生命值等于一且场上坦克数量大于零且未出生坦克数量大于一
        elif self.life == 1 and quan_var.enytank_num > 0 and quan_var.now_enytank_num > 0:
            quan_var.now_enytank_num -= 1
            self.gengxin_map_dict(0)
            self.set_xy()  # 坦克死亡后设置新出生的坦克位置
            self.again_chusheng()  # 根据位置生出坦克样式
            self.genxin_enytank_dict()
            print('坦克被击中 死亡  重新生成一个坦克')
        # 除上之外
        else:
            self.life -= 1
            self.get_life()
            # 加锁，并设置超时时间
            self.lock.acquire(timeout=0.02)
            quan_var.now_enytank_num -= 1
            # 清除enytank_dict列表中的敌方坦克
            for key, value in quan_var.enytank_dict.copy().items():
                if value == self:
                    del quan_var.enytank_dict[key]
            self.lock.release()
            self.gengxin_map_dict(0)
            self.enytank_button.setVisible(False)
            print('坦克击中 不能重新生成 场上坦克数量减一', quan_var.now_enytank_num)
            quan_var.main_obj.label_9.setText('%s'%quan_var.now_enytank_num)
            # 最后一组坦克死亡之后  清除路径
            if quan_var.now_enytank_num == 0:
                quan_var.win_music.play()
                self.win = QLabel(quan_var.frame_one)
                self.win.setGeometry(35, 150, 600, 375)
                self.win.setVisible(True)
                self.win.setStyleSheet('QLabel{border-image:url(./image/enemyTank/win.png)}')
                QApplication.processEvents()
                time.sleep(1)
                print('敌方坦克死亡 你赢了')
                sys.exit(0)
