# This file is part of MaixUI
# Copyright (c) sipeed.com
#
# Licensed under the MIT license:
#   http://www.opensource.org/licenses/mit-license.php
#

import image
import lcd
import os
import gc


class Canvas():
    def __init__(self):
        lcd.init(freq=15000000)
        lcd.clear()
        self.__w = lcd.width()
        self.__h = lcd.height()
        self.img = image.Image(size=(self.__w, self.__h))
        self.__bg_img = None
        self.__widgets = {}
        self.__bg_color = (255, 255, 255)

    def add_widget(self, widget):
        self.__widgets[widget] = widget

    def remove_widget(self, widget):
        del self.__widgets[widget]

    def set_bg_color(self, color):
        self.__bg_color = color
        self.__bg_img = None
        self.img.draw_rectangle(0, 0, self.__w, self.__h,
                                self.__bg_color, fill=True)  # background color

    def set_bg_img(self, path, padding_left=None, padding_top=None):
        self.__bg_color = None
        self.__bg_img = image.Image(
            path).resize(self.__w, self.__h)
        self.img.draw_image(self.__bg_img, 0, 0)  # background img

    def display(self):  # 10ms
        # display
        lcd.display(self.img)

    def clear(self, x, y, w, h):
        if self.__bg_color:
            self.img.draw_rectangle(
                x, y, w, h, color=self.__bg_color, fill=True)
        if self.__bg_img:
            self.img.draw_image(self.__bg_img.copy(
                (x, y, w, h), copy_to_fb=False), x, y)


ui = Canvas()

if __name__ == '__main__':
    import time
    try:
        from core import system
    except:
        from lib.core import system

    ui.set_bg_color((75, 0, 75))
    ui.set_bg_img("res/images/bg.jpg")

    clock = time.clock()
    while True:
        clock.tick()
        ui.display()
        ui.clear(440, 30, 30, 30)
        system.parallel_cycle()
        print(clock.fps())
