import os
import image

try:
    from ui_widget import Widget
    from touch import Touch,touch
    from core import system
except ImportError:
    from ui.ui_widget import Widget
    from driver.touch import touch
    from lib.core import system

class ProgessBar(Widget):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h)

        # style
        self.__panel = image.Image(size = (w, h))
        self.__background_color = (255, 255, 255)
        self.__border_color = (0, 0, 0)
        self.__border_thickness = 1
        self.__bar_color = (221, 38, 41)
        self.__bar_border_color = (0, 0, 0)
        self.__bar_border_thickness = 1

        # value
        self.__start = 0
        self.__end = 100
        self.__current = 50

    def draw(self, canvas):
        # fill background
        if self.__background_color:
            self.__panel.flood_fill(0, 0, color=self.__background_color)
        # draw border
        if self.__border_color:
            self.__panel.draw_rectangle(0, 0, self.__w, self.__h, color = self.__border_color, thickness = self.__border_thickness)
         # draw bar
        bar_x = int(self.__w * 0.025)
        bar_y = int(self.__h * 0.25)
        bar_w = int(self.__current / (self.__end - self.__start) * self.__w)
        bar_h = int(self.__h * 0.5)
        self.__panel.draw_rectangle(bar_x, bar_y, bar_w, bar_h, self.__bar_color, fill = True)
        if self.__bar_border_color:
            self.__panel.draw_rectangle(bar_x, bar_y, bar_w, bar_h, self.__bar_border_color)
        canvas.draw_img(self.__panel, self.__x, self.__y)

    def set_bg(self, color):
        self.__background_color = color
 
    def set_bg_border(self, color, thickness):
        self.__border_color = color
        self.__border_thickness = thickness

    def set_bar(self, color):
        self.__bar_color = color

    def set_bar_border(self, color, thickness):
        self.__bar_border_color = color
        self.__bar_border_thickness = thickness
    
if __name__ == '__main__':
    
    try:
        from ui_canvas import Canvas
    except:
        from ui.ui_canvas import Canvas
    # create button
    bar = ProgessBar(100, 30, 300, 20)
   
    ui = Canvas()
    
    ui.add_widget(bar)
    
    ui.set_bg_color((75, 0, 75))

    while True:
        ui.display()
        system.parallel_cycle()