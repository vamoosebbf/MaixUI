import math
import os
import image

try:
    from ui_canvas import ui
    from touch import Touch, TouchLow
    from button import sipeed_button, button_io
    from core import agent
except ImportError:
    from ui.ui_canvas import ui
    from driver.touch import Touch, TouchLow
    from driver.button import sipeed_button, button_io
    from lib.core import agent


class Button:

    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self._img = image.Image(size=(self.w, self.h))
        
        # text 
        self._text = ""
        self._text_color = (255, 255, 255)
        self._text_x = 0
        self._text_y = 0
        self._text_scale = 1

        # background
        self._background = (255, 0, 0)

        self.__eves = {Touch.press:None, Touch.release: None, Touch.idle:None}
        self.__eargs = {Touch.press:None, Touch.release: None, Touch.idle:None}
        touch.register_touch_event(self.touch_event)


    def _point_in_button(self, point):
        x = point[0]
        y = point[1]
        if x > self.x and x < self.x + self.w and y > self.y and y < self.y + self.h:
            return True
        return False
    
    def touch_event(self):
        if self._point_in_button(touch.points[0]):
            if touch.state == Touch.press and self.__eves[Touch.press] != None:
                self.__eves[Touch.press](self.__eargs[Touch.press]) if self.__eargs[Touch.press] else self.__eves[Touch.press]()
            if touch.state == Touch.release and self.__eves[Touch.release] != None:
                self.__eves[Touch.release](self.__eargs[Touch.release]) if self.__eargs[Touch.release] else self.__eves[Touch.release]()

    # eve_name: event name, string type
    def register_event(self, eve, func, *args):
        for e in self.__eves.keys():
            if e == eve:
                self.__eves[eve] = func
                self.__eargs[eve] = func
                return       
        print("cvent name error, please use follow values:")
        for i in self.__eves.keys:
            print(i)

    # align: 0 center, 1 right, 2 left
    def set_text(self, text, color=(255, 255, 255), scale = 1, padding_top = None, padding_left = None, alpha = 256):
        self._text = text
        self._text_scale = scale

        # default pos: align center
        str_w = len(self._text) * self._text_scale * 6 # 6： default char width
        str_h = self._text_scale * 10 # 10: default char height
        self._text_x = (self.w - str_w) // 2
        self._text_y = (self.h - str_h) // 2

        # custom pos
        if padding_top:
            self._text_x = padding_top
        if padding_left:
            self._text_y = padding_left
        
        self._display()
    
    def set_background(self, color):
        self._background = color
        self._display()
    
    def _display(self):
        self._img.draw_rectangle(0, 0, self.w, self.h, self._background, fill = True)
        self._img.draw_string(self._text_x, self._text_y,self._text, scale=self._text_scale, color=self._text_color)
        ui.canvas.draw_image(self._img, self.x, self.y)

touch = Touch(i2c = None, w = 480, h = 320, cycle = 200, irq_pin = 33)
    
import lcd
if __name__ == '__main__':

    lcd.init()
    ui.blank_draw()

    # create button
    btn = Button(0, 0, 80, 40)
    btn.set_text("aaa", scale = 2)
    btn.set_text("bbb", scale = 2, alpha=0)

    def on_press(self):
        btn.set_background((0,0,255))
        print("btn press")

    def on_release(self):
        btn.set_background((255, 0, 0))
        print("btn release")
    
    # register event
    btn.register_event(Touch.press, on_press)
    btn.register_event(Touch.release, on_release)

    ui.display()
    while True:
        ui.display()
    