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


class ImageBox(Widget):
    def __init__(self, x, y, w, h):
        Widget.__init__(self, x, y, w, h)
        self.__panel = None
        self._bg_color = (255, 255, 255)

        # title text
        self.__title = ""
        self.__title_scale = 1
        self.__title_x = 0
        self.__title_y = 0
        self.__title_color = (255, 255, 255)

    def set_image(self, img, padding_left=None, padding_top=None):
        self.__panel = img
        w = self.__panel.width()
        h = self.__panel.height()
        x = (self.__w - w) // 2
        y = (self.__h - h) // 2
        if padding_left:
            x = padding_left
        if padding_top:
            y = padding_top
        if self._bg_color:
            ui.img.draw_rectangle(self.__x, self.__y,
                                  self.__w, self.__h, fill=True)

        ui.img.draw_image(self.__panel, self.__x + x, self.__y + y)
        if self.__title != "":
            ui.img.draw_string(self.__title_x + self.__x, self.__title_y + self.__y,
                               self.__title, self.__title_color, scale=self.__title_scale)

    def set_title(self, title, color=(255, 255, 255), scale=1, padding_left=None, padding_top=5):
        self.__title = title
        self.__title_scale = scale
        self.__title_color = color
        tw = len(title) * 6 * self.__title_scale
        th = len(title) * 10
        self.__title_x = (self.__w - tw) // 2
        if padding_left:
            self.__title_x = padding_left
        if padding_top:
            self.__title_y = padding_top
        if self.__title != "":
            ui.img.draw_string(self.__title_x + self.__x, self.__title_y + self.__y,
                               self.__title, self.__title_color, scale=self.__title_scale)

    def set_bg_color(self, color):
        self._bg_color = color
        if self._bg_color:
            ui.img.draw_rectangle(self.__x, self.__y,
                                  self.__w, self.__h, fill=True)
        if self.__title != "":
            ui.img.draw_string(self.__title_x + self.__x, self.__title_y + self.__y,
                               self.__title, self.__title_color, scale=self.__title_scale)


if __name__ == '__main__':

    import sensor
    import time

    # sensor init
    sensor.reset()
    sensor.set_pixformat(sensor.RGB565)
    sensor.set_framesize(sensor.QVGA)
    sensor.skip_frames(time=2000)

    # create imagebox
    box = ImageBox(10, 10, 320, 300)
    box.set_title("sensor image", (0, 0, 0), 2)

    clock = time.clock()
    system.event(0, ui.display)
    while(True):
        clock.tick()
        img = sensor.snapshot()
        box.set_image(img)
        system.parallel_cycle()
        print(clock.fps())
