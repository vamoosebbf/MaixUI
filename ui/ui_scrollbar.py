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
class ScrollBar(Widget):
    def __init__(self, x, y, w, h, dir=0, track_high=0, thumb_high=0):
        super().__init__(x, y, w, h)

        # value
        self.__start = 0
        self.__end = 100
        self.__current = 50

        # style
        self.__bg_color = (255, 255, 255)
        self.__border_color = None
        self.__border_thickness = 1

        self.__thumb_color = (0, 200, 255)
        self.__thumb_border_color = (0, 0, 0)
        self.__thumb_border_thickness = 1
        self.__thumb_x = 0
        self.__thumb_y = 0
        self.__thumb_w = 0
        self.__thumb_h = 0

        # ScrollBar dir: 0: left to right 1: right to left 2: down to up 3: up to down
        self.__dir = dir

        # register press event
        self.register_event(Touch.press, self.on_press)

    def on_press(self):
        x = touch.points[1][0]
        current = int((x - self.__x) / self.__w * (self.__end - self.__start))
        self.set_value(current)

    def draw(self):
        super().draw()

        # draw bar
        ui.img.draw_rectangle(self.__bar_x + self.__x, self.__bar_y +
                              self.__y, self.__bar_w, self.__bar_h, self.__bar_color, fill=True)


if __name__ == '__main__':
    import time
    ui.set_bg_img("res/images/bg.jpg")

    # create button
    bar = ScrollBar(40, 30, 400, 20, 1)
    bar.set_bg_color((255, 255, 255))

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
        ui.display()
        system.parallel_cycle()
        print(clock.fps())
