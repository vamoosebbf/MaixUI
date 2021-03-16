import os
import image
import math
try:
    from ui_canvas import ui
    from ui_widget import Widget
    from core import system
except:
    from ui.ui_canvas import ui
    from ui.ui_widget import Widget
    from lib.core import system


class Animation:
    pi_2 = math.pi/2

    def __init__(self, widget, cycle=False):
        self.__wig = widget

        # duration: defaut 75ms
        self.__duration = 750

        # status: pos: x,y  size: w, h
        self.__start_val = [0, self.__wig.__x,
                            self.__wig.__y, self.__wig.__w, self.__wig.__h]
        self.__end_val = [1, self.__wig.__x,
                            self.__wig.__y, self.__wig.__w, self.__wig.__h]
        

        # key_vals: progress, x, y, w, h
        self.__key_vals = [self.__start_val]
        self.__key_len = 1

        #current state
        self.__index = 0
        self.__cur_val = [1, self.__wig.__x,
                            self.__wig.__y, self.__wig.__w, self.__wig.__h]
        self.__cur_diff = [1, self.__start_val[1] - self.__end_val[1],
                            self.__start_val[2] - self.__end_val[2],
                            self.__start_val[3] - self.__end_val[3],
                            self.__start_val[4] - self.__end_val[4],]

        # progress: 0(start) -> 1(end)
        self.__cycle = cycle
        setattr(self, "running", self.running_)

    # 获取列表的第一个元素
    def take_first(self, elem):
        return elem[0]

    def set_key_value_at(self, at, x, y, w, h):
        self.__key_vals.append([at*self.__duration, x, y, w, h])
        self.__key_vals.sort(key = self.take_first)
        self.__key_len = len(self.__key_vals)

    def set_start_value(self, x, y, w, h):
        self.__key_vals.append([1, x, y, w, h])
        self.__key_vals.sort(key = self.take_first)
        self.__key_len = len(self.__key_vals)

    def set_duration(self, duration):
        self.__duration = duration

    def running_(self):
        s = math.sin((self.__cur_val[0] - self.__start_val[0] ) / (self.__cur_diff[0]) * self.pi_2)
        x = int((self.__cur_diff[1]) * s + self.__start_val[1])
        y = int((self.__cur_diff[2]) * s + self.__start_val[2])
        w = int((self.__cur_diff[3]) * s + self.__start_val[3])
        h = int((self.__cur_diff[4]) * s + self.__start_val[4])
        self.__wig.set_pos_size(x, y, w, h)

        self.__cur_val[0] += 1

        # 进入下一个关键点  
        if self.__cur_val[0] > self.__end_val[0]:
            self.__index+=1
            # 完成一次动画
            if self.__index >= self.__key_len:
                if self.__cycle:
                    self.__cur_val[1:] = self.__key_vals[0][1:]
                    self.__index = 0
                    self.__cur_val[0] = 0
                else:
                    system.remove(self.running)  # stop
                    return
            self.__start_val = self.__key_vals[self.__index-1]
            self.__end_val = self.__key_vals[self.__index]
            self.__cur_diff = [self.__start_val[0] - self.__end_val[0],
                                self.__start_val[1] - self.__end_val[1],
                                self.__start_val[2] - self.__end_val[2],
                                self.__start_val[3] - self.__end_val[3],
                                self.__start_val[4] - self.__end_val[4]]

    def start(self):
        system.event(0, self.running)

    def stop(self):
        system.remove(self.running)


if __name__ == '__main__':
    import time
    import os
    import urandom as random

    ui.set_bg_color((0, 0, 0))
    
    # wig = Widget(100, 100, 20, 20)
    # wig.set_bg_color((255, 255, 0))
    # ani = Animation(wig, True)
    # ani.set_duration(100)
    # ani.set_key_value_at(0.2, 200, 200, 30, 30)
    # ani.set_key_value_at(0.1, 200, 300, 30, 30)
    # ani.set_key_value_at(0.4, 100, 200, 40, 30)
    # ani.set_key_value_at(1, 100, 100, 20, 20)

    # ani.start()
    
    for i in range(100):
        start_x = random.randint(0, 480)
        start_y = random.randint(0, 300)
        wig3 = Widget(start_x, start_y, 10, 10)
        wig3.set_bg_color(
            (random.randint(0, 255), random.randint(0, 255), 255))
        wig3.set_border((255, 255, 255), 1)
        ani3 = Animation(wig3, True)
        ani3.set_duration(30)
        ani3.set_key_value_at(0.2, random.randint(0, 480), random.randint(0, 300), 10, 10)
        ani3.set_key_value_at(0.5, random.randint(0, 480), random.randint(0, 300), 10, 10)
        ani3.set_key_value_at(1, start_x, start_y, 10, 10)
                           
        ani3.start()

    system.event(0, ui.display)
    clock = time.clock()
    while True:
        clock.tick()

        system.parallel_cycle()
        # print(clock.fps())
