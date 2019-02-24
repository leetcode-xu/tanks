from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QFrame, QDesktopWidget, QLabel
from PyQt5.QtCore import QThread, QRect
from PyQt5.QtCore import Qt
from  PyQt5 import QtGui
import sys

from Enytank import enytank
from Global import quan_var
from Mytank import mytank
from Worker import worker, worker2, worker3, work_food
from Food import food
#游戏主界面，分为左右两部分，左边进行游戏操作，右边显示得分，生命值，剩余坦克数量等显示
class main_ui(QWidget):
    def __init__(self, two = None):
        super().__init__()
        #双人游戏标志位
        self.two = two
        self.show_ui()
        quan_var.start_sound.play()
    #设置游戏边框   边框宽度为24像素
    def setBorder(self):
        self.dicts = {}
        for x in range(28):
            #上边框
            self.dicts[(x-1,-1)] = 10
            border_botton = QPushButton(self.frame_two)
            border_botton.setGeometry(x*24, 0, 24, 24)
            border_botton.setStyleSheet("QPushButton{background-color:#808080}")
            #下边框
            self.dicts[(x - 1, 26)] = 10
            border_botton_down = QPushButton(self.frame_two)
            border_botton_down.setGeometry(x * 24, 27*24, 24, 24)
            border_botton_down.setStyleSheet("QPushButton{background-color:#808080}")
        for y in range(1, 27):
            #左边框
            self.dicts[(-1, y-1)] = 10
            border_botton_left = QPushButton(self.frame_two)
            border_botton_left.setGeometry(0, y*24, 24, 24)
            border_botton_left.setStyleSheet("QPushButton{background-color:#808080}")
            #又边框
            self.dicts[(26, y-1)] = 10
            border_botton_right = QPushButton(self.frame_two)
            border_botton_right.setGeometry(27*24, y * 24, 24, 24)
            border_botton_right.setStyleSheet("QPushButton{background-color:#808080}")
        #更新地图模型，将边框添加进去
        quan_var.map_dict.update(self.dicts)
    #生成敌方坦克
    def  begin_enytank(self):
        #本想用for循环，但不知但是线程的什么机制运行不成功，如有好的方法欢迎交流
        # 初始化敌方坦克，设置在frame_two画板上
        self.enytan_obj1 = enytank(self.frame_two)
        #初始化敌方坦克工作类
        self.work1 = worker(self.enytan_obj1)
        #调用敌方坦克出生函数，随机位置显示
        self.enytan_obj1.chusheng()
        #将其生命值同步到全局变量中，存在形式  坦克对象：生命值
        quan_var.life_list[self.enytan_obj1] = self.life_1
        #显示坦克的生命值
        self.life_1.setText('%s'%self.enytan_obj1.life)
        #将start_enytank1信号绑定坦克自身的move函数
        self.work1.start_enytank1.connect(self.enytan_obj1.move)
        #初始化Qt线程
        self.thread1 = QThread()
        #将线程结束信号绑定线程退出函数，避免残留线程，
        self.work1.jieshu.connect(lambda: self.thread1.quit())
        #将工作类对象加入到线程对象中
        self.work1.moveToThread(self.thread1)
        #将线程被启动信号绑定work1类的start_enytank_thread1函数
        self.thread1.started.connect(self.work1.start_enytank_thread1)
        #启动线程
        self.thread1.start()
        #启动二号敌方坦克线程
        self.enytan_obj2 = enytank(self.frame_two)
        self.work2 = worker2(self.enytan_obj2)
        self.enytan_obj2.chusheng()
        self.life_2.setText('%s'%self.enytan_obj2.life)
        quan_var.life_list[self.enytan_obj2]=self.life_2
        self.work2.start_enytank2.connect(self.enytan_obj2.move)
        self.thread2 = QThread()
        self.work2.jieshu.connect(lambda: self.thread2.quit())
        self.work2.moveToThread(self.thread2)
        self.thread2.started.connect(self.work2.start_enytank_thread2)
        self.thread2.start()
        #启动三号敌方坦克线程
        self.enytan_obj3 = enytank(self.frame_two)
        self.work3 = worker3(self.enytan_obj3)
        self.enytan_obj3.chusheng()
        self.life_3.setText('%s' % self.enytan_obj3.life)
        quan_var.life_list[self.enytan_obj3] = self.life_3
        self.work3.start_enytank3.connect(self.enytan_obj3.move)
        self.thread3 = QThread()
        self.work3.moveToThread(self.thread3)
        self.work3.jieshu.connect(lambda: self.thread3.quit())
        self.thread3.started.connect(self.work3.start_enytank_thread3)
        self.thread3.start()

    # 生成food
    def begin_food(self):
        # 初始化一个food
        self.food_obj = food(self.frame_two)
        # 将food对象存入global中
        quan_var.food_obj = self.food_obj
        # self.food_obj.chusheng_food()
        # 实例化food工作类
        self.wf = work_food()
        # 生成一个线程对象
        self.thread_food = QThread()
        # 绑定food生成
        self.wf.start_food.connect(self.food_obj.chusheng_food)
        # 绑定food消失
        self.wf.stop_food.connect(self.food_obj.siwang)
        self.wf.moveToThread(self.thread_food)
        self.thread_food.started.connect(self.wf.work)
        self.thread_food.start()


    #初始化右边辅界面，长宽比近似黄金比例
    def show_fuui(self, Form):
        quan_var.main_obj = self
        self.frame_three = QFrame(Form)
        self.frame_three.setGeometry(QRect(672, 0, 428, 672))
        self.frame_three.setStyleSheet("background-color:#808080")
        self.frame_three.setFrameShape(QFrame.StyledPanel)
        self.frame_three.setFrameShadow(QFrame.Raised)
        self.frame_three.setObjectName("frame")
        # 坦克图标一
        self.tank_1 = QPushButton(self.frame_three)
        self.tank_1.setGeometry(QRect(65, 170, 48, 48))
        self.tank_1.setStyleSheet("color:white; border-image:url(./image/enemyTank/enemy_1_up.png)")
        self.tank_1.setObjectName("tank_1")
        # 坦克图标二
        self.tank_2 = QPushButton(self.frame_three)
        self.tank_2.setGeometry(QRect(65, 250, 48, 48))
        self.tank_2.setStyleSheet("color:white; border-image:url(./image/enemyTank/enemy_1_up.png)")
        self.tank_2.setObjectName("tank_2")
        # 坦克图标三
        self.tank_3 = QPushButton(self.frame_three)
        self.tank_3.setGeometry(QRect(65, 320, 48, 48))
        self.tank_3.setStyleSheet("color:white; border-image:url(./image/enemyTank/enemy_1_up.png)")
        self.tank_3.setObjectName("tank_3")
        #玩家图标一
        self.ourtank_1 = QPushButton(self.frame_three)
        self.ourtank_1.setGeometry(QRect(65, 390, 48, 48))
        self.ourtank_1.setStyleSheet("color:white; border-image:url(./image/myTank/tank_up.png)")
        self.ourtank_1.setObjectName("ourtank_1")
        #玩家图标二
        self.ourtank_2 = QPushButton(self.frame_three)
        self.ourtank_2.setGeometry(QRect(65, 460, 48, 48))
        self.ourtank_2.setStyleSheet("color:white; border-image:url(./image/myTank/tank_two_up.png)")
        self.ourtank_2.setObjectName("ourtank_2")
        #敌方坦克一的剩余生命
        self.life_1 = QLabel(self.frame_three)
        self.life_1.setGeometry(QRect(210, 170, 200, 48))
        font = QtGui.QFont()
        font.setPointSize(25)
        self.life_1.setFont(font)
        self.life_1.setStyleSheet("color:white")
        self.life_1.setObjectName("life_1")
        # 敌方坦克二的剩余生命
        self.life_2 = QLabel(self.frame_three)
        self.life_2.setGeometry(QRect(210, 250, 200, 48))
        font = QtGui.QFont()
        font.setPointSize(25)
        self.life_2.setFont(font)
        self.life_2.setStyleSheet("color:white")
        self.life_2.setObjectName("life_2")
        # 敌方坦克三的剩余生命
        self.life_3 = QLabel(self.frame_three)
        self.life_3.setGeometry(QRect(210, 320, 200, 48))
        font = QtGui.QFont()
        font.setPointSize(25)
        self.life_3.setFont(font)
        self.life_3.setStyleSheet("color:white")
        self.life_3.setObjectName("life_3")
        #我方玩家一的生命值
        self.ourlife_1 = QLabel(self.frame_three)
        self.ourlife_1.setGeometry(QRect(210, 390, 200, 48))
        font = QtGui.QFont()
        font.setPointSize(25)
        self.ourlife_1.setFont(font)
        self.ourlife_1.setStyleSheet("color:white")
        self.ourlife_1.setObjectName("ourlife_1")
        #我方玩家二的生命值
        self.ourlife_2 = QLabel(self.frame_three)
        self.ourlife_2.setGeometry(QRect(210, 460, 200, 48))
        font = QtGui.QFont()
        font.setPointSize(25)
        self.ourlife_2.setFont(font)
        self.ourlife_2.setStyleSheet("color:white")
        self.ourlife_2.setObjectName("ourlife_2")
        self.ourlife_2.setObjectName("ourlife_2")
        #游戏分数文字
        self.game_text = QLabel(self.frame_three)
        self.game_text.setGeometry(QRect(65, 40, 100, 100))
        font = QtGui.QFont()
        font.setPointSize(30)
        self.game_text.setFont(font)
        self.game_text.setStyleSheet("color:white")
        self.game_text.setText('分数')
        self.game_text.setObjectName("game_text")
        #游戏分数
        self.game_zhi = QLabel(self.frame_three)
        self.game_zhi.setGeometry(QRect(210, 40, 200, 100))
        font = QtGui.QFont()
        font.setPointSize(30)
        self.game_zhi.setFont(font)
        self.game_zhi.setStyleSheet("color:white")
        self.game_zhi.setText('0')
        self.game_zhi.setObjectName("game_zhi")
        #剩余坦克数量
        self.label_8 = QLabel(self.frame_three)
        self.label_8.setGeometry(QRect(65, 550, 350, 48))
        self.label_8.setText('剩余坦克')
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label_8.setFont(font)
        self.label_8.setStyleSheet("color:white")
        self.label_8.setObjectName("label_8")
        #显示剩余坦克数量的值
        self.label_9 = QLabel(self.frame_three)
        self.label_9.setGeometry(QRect(210, 550, 350, 48))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_9.setFont(font)
        self.label_9.setWhatsThis("")
        self.label_9.setStyleSheet("color:white")
        self.label_9.setText('%s'%quan_var.enytank_num)
        self.label_9.setObjectName("label_8")
        # self.label_8.setVisible(True)
    #根据计算机屏幕分辨率计算，使其依然居中显示
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def show_ui(self):
        #游戏界面大小，也是近似黄金比例
        self.resize(1100, 672)
        #将游戏界面水平、垂直居中
        self.center()
        self.frame_one = QFrame(self)
        self.frame_one.setGeometry( 0,  0, 672, 672)
        self.setFocus() #把self界面设置为焦点，以响应键盘事件
        #初始化一个正方形的游戏操作界面
        self.frame_two = QFrame(self.frame_one)
        self.frame_two.setGeometry(0, 0, 672, 672)
        quan_var.frame_one = self.frame_one
        #调用游戏辅界面
        self.show_fuui(self)
        self.frame_one.setStyleSheet('QWidget{background-color:black;}') #设置黑色背景
        self.setBorder()  #设置边框
        self.tank_per1 = mytank(17*24, 25*24)
        self.tank_per1.chusheng(self.frame_two) #玩家一出生
        self.ourlife_1.setText("%s" % self.tank_per1.life)  #显示其生命值
        quan_var.life_list[self.tank_per1] = self.ourlife_1
        if self.two:
            self.tank_per2 = mytank(9*24, 25*24, 'tank_two')
            self.tank_per2.chusheng(self.frame_two) #玩家二出生
            self.ourlife_2.setText("%s"%self.tank_per2.life)
            quan_var.life_list[self.tank_per2]=self.ourlife_2

        laoying = QPushButton(self.frame_two)  #老鹰定位
        quan_var.laoying = laoying             #同步老鹰对象到全局变量中
        laoying.setGeometry(13*24, 25*24, 48, 48)
        laoying.setStyleSheet('QPushButton{border-image:url(./image/home/home1.png);}')
        quan_var.static_obj[(13*24, 25*24)] = laoying  #记录老鹰位置和对象，老鹰模型是2格*2格，所以需要记录四个位置
        quan_var.static_obj[(14*24, 25*24)] = laoying
        quan_var.static_obj[(13*24, 26*24)] = laoying
        quan_var.static_obj[(14*24, 26*24)] = laoying
        #初始化游戏界面中的土砖、树木、钢墙
        for y in range(1, 27):
            for x in range(1, 27):
                pixel = quan_var.map_dict.get((x-1,y-1),0)
                if pixel == 0:
                    pass
                elif pixel == quan_var.brick:  # 土砖
                    # print(pixel)
                    pushbutton_brick = QPushButton(self.frame_two)
                    pushbutton_brick.setGeometry(x*24, y*24, 24, 24)
                    pushbutton_brick.setText('')
                    pushbutton_brick.setStyleSheet('QPushButton{border-image:url(./image/scene/brick.png)}')
                    quan_var.static_obj[(x*24, y*24)] = pushbutton_brick
                elif pixel == quan_var.tree:  # 树木
                    pushbutton_brick = QPushButton(self.frame_one)
                    pushbutton_brick.setGeometry(x * 24, y * 24, 24, 24)
                    pushbutton_brick.setText('')
                    pushbutton_brick.setStyleSheet('QPushButton{border-image:url(./image/scene/tree.png)}')
                    quan_var.static_obj[(x * 24, y * 24)] = pushbutton_brick
                elif pixel == quan_var.iron: #钢墙
                    pushbutton_brick = QPushButton(self.frame_two)
                    pushbutton_brick.setGeometry(x * 24, y * 24, 24, 24)
                    pushbutton_brick.setText('')
                    pushbutton_brick.setStyleSheet('QPushButton{border-image:url(./image/scene/iron.png)}')
                    quan_var.static_obj[(x * 24, y * 24)] = pushbutton_brick
        # 生成敌方坦克
        # self.begin_enytank()
        #设置frame画板的透明度为百分之50
        # self.frame_one.setWindowOpacity(0.5)
        #初始化一个food线程
        self.begin_food()
        # self.food_obj = food(self.frame_two)
        # quan_var.food_obj = self.food_obj
        # self.food_obj.chusheng_food()
    #覆写点击关闭事件
    def closeEvent(self, QCloseEvent):
        # 未做出对正在运行线程的处理
        self.close()
        sys.exit(0)
    #键盘响应事件函数
    def keyPressEvent(self, e):
        if e.key()==Qt.Key_Right:
            #玩家一往右行走
            self.tank_per1.move((1, 0))
        elif e.key()==Qt.Key_Up:
            #玩家一往上移动
            self.tank_per1.move((0, -1))
        elif e.key()==Qt.Key_Down:
            #玩家一往下
            self.tank_per1.move((0, 1))
        elif e.key()==Qt.Key_Left:
            #玩家往左移动
            self.tank_per1.move((-1, 0))
        # elif e.key()==Qt.Key_0:
        elif e.key()==Qt.Key_Space:
            #我方坦克一发射子弹
            self.tank_per1.fashe()
        elif self.two and e.key()==Qt.Key_D:
            #玩家二往右行走
            self.tank_per2.move((1, 0))
        elif self.two and e.key()==Qt.Key_W:
            #玩家二往上移动
            self.tank_per2.move((0, -1))
        elif self.two and e.key()==Qt.Key_S:
            #玩家二往下
            self.tank_per2.move((0, 1))
        elif self.two and e.key()==Qt.Key_A:
            #玩家往左移动
            self.tank_per2.move((-1, 0))
        elif self.two and e.key()==Qt.Key_J:
            #玩家二发射子弹
            self.tank_per2.fashe()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    m = main_ui()
    m.show()
    sys.exit(app.exec_())


