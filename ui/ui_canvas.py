# This file is part of MaixUI
# Copyright (c) sipeed.com
#
# Licensed under the MIT license:
#   http://www.opensource.org/licenses/mit-license.php
#

import image, lcd, os, gc

class Canvas():
    def __init__(self):
        lcd.init(freq=15000000)
        self.__w = lcd.width()
        self.__h = lcd.height()
        self.img = image.Image(size=(self.__w, self.__h))
        self.__widgets = {}
        self.__bg_color = None
        self.__bg_img_path = None
        self.__bg_img_padding_left = None
        self.__bg_img_padding_top = None
        
    def add_widget(self, widget):
        self.__widgets[widget] = widget
    
    def remove_widget(self, widget):
        del self.__widgets[widget]

    def set_bg_color(self, color):
        self.__bg_color = color

        
    def set_bg_img(self, path, padding_left = None, padding_top = None):
        self.__bg_img_path = path
        img = image.Image(self.__bg_img_path)
        w = img.width()
        h = img.height()
        del img
        
        # default center
        self.__bg_img_padding_left = (self.__w - w) // 2
        self.__bg_img_padding_top = (self.__h - h) // 2

        # custom pos
        if padding_left:
            self.__bg_img_padding_left = padding_left
        if padding_top:
            self.__bg_img_padding_top = padding_top

    def draw_img(self, *args, **kwargs):
        self.img.draw_image(*args, **kwargs)
    
    def display(self):  # 10ms
        # draw self
        if self.__bg_img_path and self.__bg_color == None:
            self.img.draw_image(image.Image(self.__bg_img_path),self.__bg_img_padding_left, self.__bg_img_padding_top, alpha=255)
        elif self.__bg_color and self.__bg_img_path == None:
            self.img.draw_rectangle(0, 0, self.__w, self.__h, self.__bg_color, fill = True)
        elif self.__bg_color and self.__bg_img_path:
            self.img.draw_rectangle(0, 0, self.__w, self.__h, self.__bg_color, fill = True) # background color
            self.img.draw_image(image.Image(self.__bg_img_path), self.__bg_img_padding_left, self.__bg_img_padding_top) # background img
        
        #draw widgets
        for widget in self.__widgets.values():
            widget.draw(self)
        
        # display
        lcd.display(self.img)

if __name__ == '__main__':
    import time
    try:
        from core import system
    except:
        from lib.core import system

    ui = Canvas()
    
    ui.set_bg_color((75, 0, 75))

    clock = time.clock()
    while True:
        clock.tick()
        ui.display()
        system.parallel_cycle()
        print(clock.fps())