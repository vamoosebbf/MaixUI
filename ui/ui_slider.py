import os
import image
try:
    from ui_progress_bar import ProgressBar
    from ui_canvas import ui
    from core import system
except:
    from ui.ui_prgress_bar import ProgressBar
    from ui.ui_canvas import ui
    from lib.core import system


class Slider(ProgressBar):
    def __init__(self, x, y, w, h, dir=0):
        super().__init__(x, y, w, h, dir)
        # handle： 触球
        self.__handle_color = (221, 38, 41)
        self.__handle_w = 0
        self.__handle_h = 0
        self.__handle_border_color = None
        self.__handle_border_thickness = 1

    def draw(self):
        super().draw()
        if self.__dir == 0:
            self.__handle_w = int(self.__h * 0.6)
            self.__handle_h = self.__handle_w
            handle_x = int(self.__bar_w)
            handle_y = int((self.__h - self.__handle_h) * 0.5)
        elif self.__dir == 1:
            self.__handle_w = int(self.__h * 0.6)
            self.__handle_h = self.__handle_w
            handle_x = int(self.__bar_x - self.__handle_w/2)
            handle_y = int((self.__h - self.__handle_h) * 0.5)
        elif self.__dir == 3:
            self.__handle_w = int(self.__w * 0.6)
            self.__handle_h = self.__handle_w
            handle_x = int((self.__w - self.__handle_w) * 0.5)
            handle_y = int(self.__bar_h)
        elif self.__dir == 2:
            self.__handle_w = int(self.__w * 0.6)
            self.__handle_h = self.__handle_w
            handle_x = int((self.__w - self.__handle_w) * 0.5)
            handle_y = int(self.__bar_y - self.__handle_h/2)

        ui.canvas.draw_rectangle(handle_x + self.__x, handle_y + self.__y,
                              self.__handle_w, self.__handle_h, color=self.__handle_color, fill=True)


if __name__ == '__main__':

    import time
    from ui_label import Label
    ui.set_bg_color((75, 0, 75))
    ui.set_bg_img("res/images/bg.jpg")
    # create button
    bar = Slider(20, 30, 30, 400, 3)
    bar.set_bg_color((255, 255, 255))

    bar.set_value(100)

    lab = Label(400, 60, 30, 30)

    clock = time.clock()
    system.event(1, ui.display)
    val = 1
    dir = True
    while True:
        clock.tick()
        if dir:
            val += 1
        else:
            val -= 1
        if val == 100:
            dir = False
        if val == 0:
            dir = True
        bar.set_value(val)
        lab.set_text(str(bar.__current) + "%")
        system.parallel_cycle()
        # print(clock.fps())
