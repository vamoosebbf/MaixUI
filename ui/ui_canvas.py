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
        from Maix import utils
        import machine

        if utils.gc_heap_size() != 1024*1024:
            utils.gc_heap_size(1024*1024) # 1MiB
            machine.reset()
        lcd.init(freq=15000000)
        lcd.clear()
        self.__w = lcd.width()
        self.__h = lcd.height()
        self.canvas = image.Image(size=(self.__w, self.__h))
        self.__bg_img = None
        self.__widgets = {}
        self.__bg_color = (255, 255, 255)
        self.canvas.draw_rectangle(0, 0, self.__w, self.__h,
                                self.__bg_color, fill=True)  # background color

    def add_widget(self, widget):
        self.__widgets[widget] = widget

    def remove_widget(self, widget):
        del self.__widgets[widget]

    def set_bg_color(self, color):
        self.__bg_color = color
        self.__bg_img = None
        self.canvas.draw_rectangle(0, 0, self.__w, self.__h,
                                self.__bg_color, fill=True)  # background color

    def set_bg_img(self, img, padding_left=None, padding_top=None):
        self.__bg_color = None
        self.__bg_img = img.resize(self.__w, self.__h)
        self.canvas.draw_image(self.__bg_img, 0, 0)  # background img

    def display(self):  # 10ms
        # display
        lcd.display(self.canvas)

    def clear(self, x, y, w, h):
        if self.__bg_color:
            self.canvas.draw_rectangle(
                x, y, w, h, color=self.__bg_color, fill=True)
        elif self.__bg_img:
            try:
                self.canvas.draw_image(self.__bg_img.copy(
                    (x, y, w, h), copy_to_fb=False), x, y)
            except: # if  roi is (0, 0, 0, 0)
                pass

ui = Canvas()

if __name__ == '__main__':
    import time
    try:
        from core import system
    except:
        from lib.core import system
    img = image.Image("res/images/bg.jpg")
    ui.set_bg_img(img)

    clock = time.clock()
    while True:
        clock.tick()
        ui.display()
        ui.clear(0, 0, 0, 0)
        system.parallel_cycle()
        print(clock.fps())
