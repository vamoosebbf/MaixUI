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
        self.__bar_x = 0
        self.__bar_y = 0
        self.__bar_w = 0
        self.__bar_h = 0
        # progressbar dir: 0: left to right 1: right to left 2: low to high 3: high to low
        self.__dir = dir
        # register press event
        self.register_event(Touch.press, self.on_press)

    def on_press(self):
        if self.__dir == 0:
            x = touch.points[1][0]
            current = int((x - self.__x) / self.__w *
                          (self.__end - self.__start))
        elif self.__dir == 1:
            x = touch.points[1][0]
            current = int((self.__x + self.__w - x) / self.__w *
                          (self.__end - self.__start))
        elif self.__dir == 2:
            y = touch.points[1][1]
            current = int((self.__h - y + self.__y) / self.__h *
                          (self.__end - self.__start))
            print(current)
        elif self.__dir == 3:
            y = touch.points[1][1]
            current = int((y - self.__y) / self.__h *
                          (self.__end - self.__start))

        self.set_value(current)

    def draw(self):
        super().draw()
        if self.__dir == 3:
            self.__bar_x = int(self.__w * 0.3)
            self.__bar_y = int(self.__w * 0.3)
            self.__bar_w = int(self.__w * 0.4)
            self.__bar_h = int(self.__current / (self.__end -
                                                 self.__start) * (self.__h - self.__bar_x*2))
            if self.__bar_border_color:
                ui.img.draw_rectangle(int(self.__x + self.__bar_x),
                                      int(self.__y + self.__bar_y),
                                      self.__bar_w,
                                      int(self.__h - self.__bar_x*2),
                                      self.__bar_border_color)
        elif self.__dir == 2:
            self.__bar_w = int(self.__w * 0.4)
            self.__bar_h = int(self.__current / (self.__end -
                                                 self.__start) * (self.__h - self.__bar_x*2))
            self.__bar_x = int(self.__w * 0.3)
            self.__bar_y = int(self.__h - self.__bar_h - self.__w * 0.3)
            if self.__bar_border_color:
                ui.img.draw_rectangle(int(self.__x + self.__bar_x),
                                      int(self.__y + self.__bar_x),
                                      self.__bar_w,
                                      int(self.__h - self.__bar_x*2),
                                      self.__bar_border_color)
        elif self.__dir == 1:
            self.__bar_w = int(self.__current / (self.__end -
                                                 self.__start) * (self.__w - self.__h * 0.3*2))
            self.__bar_h = int(self.__h * 0.4)
            self.__bar_x = int(self.__w - self.__bar_w - self.__h * 0.3)
            self.__bar_y = int(self.__h * 0.3)
            if self.__bar_border_color:
                ui.img.draw_rectangle(self.__x + self.__bar_y, self.__y +
                                      self.__bar_y,
                                      int((self.__w - self.__h * 0.3*2)),
                                      int(self.__h * 0.4),
                                      self.__bar_border_color)
        elif self.__dir == 0:
            self.__bar_x = int(self.__h * 0.3)
            self.__bar_y = int(self.__h * 0.3)
            self.__bar_w = int(self.__current / (self.__end -
                                                 self.__start) * (self.__w - self.__bar_x*2))
            self.__bar_h = int(self.__h * 0.4)
            if self.__bar_border_color:
                ui.img.draw_rectangle(self.__x + self.__bar_x, self.__y +
                                      self.__bar_y,
                                      int(self.__w - self.__bar_x * 2),
                                      int(self.__h * 0.4),
                                      self.__bar_border_color)
        # draw bar
        ui.img.draw_rectangle(self.__bar_x + self.__x, self.__bar_y +
                              self.__y, self.__bar_w, self.__bar_h, self.__bar_color, fill=True)

    def set_range(self, start, end):
        self.__start = start
        self.__end = end

    def set_value(self, val):
        self.clear()
        self.__current = val
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

    # # create button
    bar1 = ProgressBar(40, 280, 400, 30, 0)
    bar1.set_bg_color((255, 255, 255))
    bar2 = ProgressBar(40, 240, 400, 30, 1)
    bar2.set_bg_color((255, 255, 255))
    bar3 = ProgressBar(440, 20, 30, 200, 2)
    bar3.set_bg_color((255, 255, 255))
    bar6 = ProgressBar(40, 20, 30, 200, 3)
    bar6.set_bg_color((255, 255, 255))

    system.event(0, ui.display)
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
        bar1.set_value(val)
        bar2.set_value(val)
        bar3.set_value(val)
        bar6.set_value(val)
        system.parallel_cycle()
        print(clock.fps())
