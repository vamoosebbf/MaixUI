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
        self.__start_val = [self.__wig.__x,
                            self.__wig.__y, self.__wig.__w, self.__wig.__h]
        self.__end_val = [0, 0, 0, 0]
        # key_vals: at, x, y, w, h
        self.__key_vals = []

        # progress: 0(start) -> 1(end)
        self.__progress = 0
        self.__cycle = cycle
        setattr(self, "running", self.running_)

    def set_key_value_at(self, at, x, y, w, h):
        self.__key_vals.append([at, x, y, w, h])

    def set_start_value(self, x, y, w, h):
        self.__start_val = [x, y, w, h]

    def set_end_value(self, x, y, w, h):
        self.__end_val = [x, y, w, h]

    def set_duration(self, duration):
        self.__duration = duration

    def running_(self):
        s = math.sin(self.__progress / self.__duration * self.pi_2)
        x = int((self.__end_val[0] - self.__start_val[0])
                * s + self.__start_val[0])
        y = int((self.__end_val[1] - self.__start_val[1])
                * s + self.__start_val[1])
        w = int((self.__end_val[2] - self.__start_val[2])
                * s + self.__start_val[2])
        h = int((self.__end_val[3] - self.__start_val[3])
                * s + self.__start_val[3])
        self.__wig.set_pos_size(x, y, w, h)
        self.__progress += 1
        if self.__progress > self.__duration:
            if self.__cycle:
                self.__progress = 0  # restart
            else:
                system.remove(self.running)  # stop

    def start(self):
        system.event(0, self.running)

    def stop(self):
        system.remove(self.running)


if __name__ == '__main__':
    import time
    import os
    import urandom as random

    ui.set_bg_color((0, 0, 0))

    for i in range(200):
        wig3 = Widget(random.randint(0, 480), random.randint(0, 300), 10, 10)
        wig3.set_bg_color(
            (random.randint(0, 255), random.randint(0, 255), 255))
        wig3.set_border((255, 255, 255), 1)
        ani3 = Animation(wig3, 1)
        ani3.set_duration(30)
        ani3.set_end_value(random.randint(0, 480),
                           random.randint(0, 300), 10, 10)
        ani3.start()

    system.event(0, ui.display)
    clock = time.clock()

    while True:
        clock.tick()

        system.parallel_cycle()
        # print(clock.fps())
