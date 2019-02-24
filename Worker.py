import time
import random
from PyQt5.QtCore import QObject, pyqtSignal

from Global import quan_var

#敌方一号坦克工作线程类
class worker(QObject):
    fa_bullet_eny = pyqtSignal()
    fa_bullet = pyqtSignal()
    start_enytank1 = pyqtSignal()
    jieshu = pyqtSignal()
    def __init__(self, obj=None):
        self.obj_enytank = obj
        super().__init__()
    #每过0.8秒发送一个信号，让坦克移动一个基本单位
    def start_enytank_thread1(self):
        while self.obj_enytank.life:
            self.start_enytank1.emit()
            time.sleep(0.8)
            # print('fa she start_enytank xin hao1')
        self.jieshu.emit()
#敌方二号坦克工作线程类
class worker2(QObject):
    fa_bullet = pyqtSignal()
    start_enytank2 = pyqtSignal()
    jieshu = pyqtSignal()

    def __init__(self, obj=None):
        self.obj_enytank = obj
        super().__init__()

    # 每过1.2秒发送一个信号，让坦克移动一个基本单位
    def start_enytank_thread2(self):
        while self.obj_enytank.life:
            self.start_enytank2.emit()
            time.sleep(1.2)
            # print('fa she start_enytank xin hao2')
        self.jieshu.emit()
#敌方三号坦克工作线程类
class worker3(QObject):
    start_enytank3 = pyqtSignal()
    jieshu = pyqtSignal()
    def __init__(self, obj=None):
        self.obj_enytank = obj
        super().__init__()
    # 每过1秒发送一个信号，让坦克移动一个基本单位
    def start_enytank_thread3(self):
        while self.obj_enytank.life:
            self.start_enytank3.emit()
            time.sleep(1)
            # print('fa she start_enytank xin hao3')
        self.jieshu.emit()
#子弹工作线程
class work_bullet(QObject):
    fa_bullet_singnal = pyqtSignal()
    jieshu1 = pyqtSignal()
    jieshu = pyqtSignal()
    fa_bullet_eny = pyqtSignal()
    def __init__(self, obj):
        super().__init__()
        self.obj = obj
    #敌方子弹没0.05秒移动一个基本单位
    def fa_bullet_enytank(self):
        # self.fa_bullet_eny.emit()
        while self.obj.life:
            self.fa_bullet_eny.emit()
            time.sleep(0.05)
        # 子弹生命标记为False，发送结束线程信号，结束线程
        self.jieshu.emit()
    #我方子弹每0.05秒移动一个基本单位
    def fa_bullet(self):
        while self.obj.life:
            self.fa_bullet_singnal.emit()
            time.sleep(0.05)
        #子弹生命标记为False，发送结束线程信号，结束线程
        self.jieshu1.emit()
        #用于表示线程子弹线程已经结束，不设置标志位，高并发的时候容易出错
        quan_var.thread_life = False
        # print('发射jieshu1信号')
# 食物工作类
class work_food(QObject):
    start_food = pyqtSignal()
    stop_food = pyqtSignal()

    def work(self):
        while True:
            self.start_food.emit()
            time.sleep(15)
            self.stop_food.emit()
            time.sleep(random.randint(3, 10))
