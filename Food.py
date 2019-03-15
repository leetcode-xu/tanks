from PyQt5.QtWidgets import QWidget,QPushButton
import random

from Global import quan_var


class food:
    def __init__(self, frame=0):
        self.frame = frame
        self.life = False
        self.show_time = 10
        #间隔时间
        self.takt_time = 30
        self.food_type = 0.1

    def get_x(self):
        self.x = random.randint(0, 25)
        return self.x * 24 + 24

    def get_y(self):
        self.y = random.randint(0, 25)
        return self.y * 24 + 24

    def get_food(self):
        # 手雷     五角星    生命值
        foods = ['boom', 'star', 'tank']
        food = random.choice(foods)
        self.food_type = (foods.index(food) + 1)/10
        # print(self.food_type)
        return food

    def update_flag(self):
        if quan_var.map_dict.get((self.x, self.y), 0) <= 1:
            quan_var.map_dict[(self.x, self.y)] = self.food_type
        if quan_var.map_dict.get((self.x + 1, self.y), 0) <= 1:
            quan_var.map_dict[(self.x + 1, self.y)] = self.food_type
        if quan_var.map_dict.get((self.x, self.y + 1), 0) <= 1:
            quan_var.map_dict[(self.x, self.y + 1)] = self.food_type
        if quan_var.map_dict.get((self.x + 1, self.y + 1), 0) <= 1:
            quan_var.map_dict[(self.x + 1, self.y + 1)] = self.food_type

    def clear_flag(self):
        if quan_var.map_dict.get((self.x, self.y), 0) < 1:
            quan_var.map_dict[(self.x, self.y)] = 0
        if quan_var.map_dict.get((self.x + 1, self.y), 0) < 1:
            quan_var.map_dict[(self.x + 1, self.y)] = 0
        if quan_var.map_dict.get((self.x, self.y + 1), 0) < 1:
            quan_var.map_dict[(self.x, self.y + 1)] = 0
        if quan_var.map_dict.get((self.x + 1, self.y + 1), 0) < 1:
            quan_var.map_dict[(self.x + 1, self.y + 1)] = 0

    def add_food(self):
        self.food_icon.setGeometry(self.get_x(), self.get_y(), 44, 44)
        self.food_icon.setStyleSheet(r'QPushButton{border-image:url(./image/food/food_%s.png)}'%self.get_food())
        self.food_icon.setVisible(True)
        self.update_flag()
        self.life = True

    def set_food_dict(self):
        quan_var.food_dict = {}
        quan_var.food_dict[(self.x * 24 + 24, self.y * 24 + 24)] = self
        quan_var.food_dict[(self.x * 24 + 48, self.y * 24 + 24)] = self
        quan_var.food_dict[(self.x * 24 + 24, self.y * 24 + 48)] = self
        quan_var.food_dict[(self.x * 24 + 48, self.y * 24 + 48)] = self


    def siwang(self):
        self.life = False
        self.clear_flag()
        self.food_icon.setVisible(False)

    def chusheng_food(self):
        self.life = True
        self.food_icon = QPushButton(self.frame)
        while True:
            x = self.get_x()
            y = self.get_y()
            if not (quan_var.map_dict.get((self.x, self.y), 0) and quan_var.map_dict.get((self.x + 1, self.y), 0) and\
                quan_var.map_dict.get((self.x, self.y + 1), 0) and quan_var.map_dict.get((self.x + 1, self.y + 1), 0)):
                self.food_icon.setGeometry(x, y, 44, 44)
                break
        self.food_icon.setStyleSheet(r'QPushButton{border-image:url(./image/food/food_%s.png)}'%self.get_food())
        self.update_flag()
        self.food_icon.setVisible(True)


if __name__ == '__main__':
    p = food()
    print(p.get_food())


