import os
import image

try:
    from ui_canvas import ui
    from ui_widget import Widget
    from touch import Touch, touch
    from core import system
except ImportError:
    from ui.ui_canvas import ui
    from ui.ui_widget import Widget
    from driver.touch import touch
    from lib.core import system

# 进度条


class ProgressBar(Widget):
    def __init__(self, x, y, w, h, dir=0):
        super().__init__(x, y, w, h)

        # value
        self.__start = 0
        self.__end = 100
        self.__current = 50

        # style
        self.__bg_color = (255, 255, 255)
        self.__border_color = None
        self.__border_thickness = 1
        self.__bar_color = (0, 200, 255)
        self.__bar_border_color = (0, 0, 0)
        self.__bar_border_thickness = 1
        self.__bar_x = int(self.__w * 0.025)
        self.__bar_y = int(self.__h * 0.4)
        self.__bar_w = int(self.__current / (self.__end -
                                             self.__start) * self.__w * 0.95)
        self.__bar_h = int(self.__h * 0.2)
        self.__dir = dir  # 0: left to right 1: right to left 2: down to up 3: up to down

        # register press event
        self.register_event(Touch.press, self.on_press)

    def on_press(self):
        x = touch.points[1][0]
        current = int((x - self.__x) / self.__w * (self.__end - self.__start))
        self.set_value(current)

    def draw(self):
        super().draw()

        # draw border
        if self.__border_color:
            ui.img.draw_rectangle(self.__x, self.__y, self.__w, self.__h,
                                  color=self.__border_color, thickness=self.__border_thickness)
        if self.__dir == 3:
            self.__bar_w = int(self.__w * 0.2)
            self.__bar_h = int(self.__current / (self.__end -
                                                 self.__start) * self.__h * 0.95)
            self.__bar_x = int(self.__w * 0.4)
            self.__bar_y = int(self.__h * 0.025)
        elif self.__dir == 2:
            self.__bar_w = int(self.__w * 0.2)
            self.__bar_h = int(self.__current / (self.__end -
                                                 self.__start) * self.__h * 0.95)
            self.__bar_x = int(self.__w * 0.4)
            self.__bar_y = int(self.__h - self.__bar_h - self.__h * 0.025)
        elif self.__dir == 1:
            self.__bar_w = int(self.__current / (self.__end -
                                                 self.__start) * self.__w * 0.95)
            self.__bar_h = int(self.__h * 0.2)
            self.__bar_x = int(self.__w - self.__bar_w - self.__w * 0.025)
            self.__bar_y = int(self.__h * 0.4)

        if self.__dir == 2 or self.__dir == 3:
            if self.__bar_border_color:
                ui.img.draw_rectangle(int(self.__x + self.__w * 0.4), int(self.__y + self.__h * 0.025), int(
                    self.__w * 0.2), int(self.__h * 0.95), self.__bar_border_color)

        if self.__dir == 1 or self.__dir == 0:
            if self.__bar_border_color:
                ui.img.draw_rectangle(int(self.__x + self.__w * 0.025), int(self.__y +
                                                                            self.__h * 0.4),
                                      int(self.__w * 0.95), int(self.__h * 0.2), self.__bar_border_color)

        # draw bar
        ui.img.draw_rectangle(self.__bar_x + self.__x, self.__bar_y +
                              self.__y, self.__bar_w, self.__bar_h, self.__bar_color, fill=True)

    def set_range(self, start, end):
        self.__start = start
        self.__end = end
        self.__bar_w = int(self.__current / (self.__end -
                                             self.__start) * self.__w * 0.95)

    def set_value(self, val):
        self.clear()
        self.__current = val
        self.__bar_w = int(self.__current / (self.__end -
                                             self.__start) * self.__w * 0.95)
        self.draw()

    def set_bg_border(self, color, thickness):
        self.__border_color = color
        self.__border_thickness = thickness
        self.draw()

    def set_bar_color(self, color):
        self.__bar_color = color
        self.draw()

    def set_bar_border(self, color, thickness):
        self.__bar_border_color = color
        self.__bar_border_thickness = thickness
        self.draw()

    def get_value(self):
        return self.__current


if __name__ == '__main__':
    import time
    ui.set_bg_color((75, 0, 75))
    ui.set_bg_img("res/images/bg.jpg")

    # create button
    bar = ProgressBar(40, 30, 400, 20, 1)
    bar.set_bg_color((255, 255, 255))
    bar1 = ProgressBar(40, 70, 400, 20, 0)
    bar1.set_bg_color((255, 255, 255))
    bar2 = ProgressBar(40, 100, 400, 20, 1)
    bar2.set_bg_color((255, 255, 255))
    bar3 = ProgressBar(440, 20, 20, 200, 2)
    bar3.set_bg_color((255, 255, 255))
    bar4 = ProgressBar(40, 170, 400, 20, 0)
    bar4.set_bg_color((255, 255, 255))
    bar5 = ProgressBar(40, 210, 400, 20, 1)
    bar5.set_bg_color((255, 255, 255))
    bar6 = ProgressBar(40, 20, 20, 200, 3)
    bar6.set_bg_color((255, 255, 255))

    bar.set_value(100)
    # system.event(1, ui.display)
    clock = time.clock()
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
        bar1.set_value(val)
        bar2.set_value(val)
        bar3.set_value(val)
        bar4.set_value(val)
        bar5.set_value(val)
        bar6.set_value(val)
        ui.display()
        system.parallel_cycle()
        print(clock.fps())
