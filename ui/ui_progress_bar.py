import os
import image

try:
    from ui_canvas import ui
    from ui_widget import Widget
    from touch import Touch,touch
    from core import system
except ImportError:
    from ui.ui_canvas import ui
    from ui.ui_widget import Widget
    from driver.touch import touch
    from lib.core import system

# 进度条
class ProgressBar(Widget):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h)

        # value
        self.__start = 0
        self.__end = 100
        self.__current = 50

        # style
        self.__bg_color = (255, 255, 255)
        self.__border_color = None
        self.__border_thickness = 1
        self.__bar_color = (221, 38, 41)
        self.__bar_border_color = None
        self.__bar_border_thickness = 1
        self.__bar_x = int(self.__w * 0.025)
        self.__bar_y = int(self.__h * 0.25)
        self.__bar_w = int(self.__current / (self.__end - self.__start) * self.__w * 0.95)
        self.__bar_h = int(self.__h * 0.5)
        
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
            ui.img.draw_rectangle(self.__x, self.__y, self.__w, self.__h, color = self.__border_color, thickness = self.__border_thickness)

         # draw bar
        ui.img.draw_rectangle(self.__bar_x + self.__x, self.__bar_y + self.__y, self.__bar_w, self.__bar_h, self.__bar_color, fill = True)
        if self.__bar_border_color:
            ui.img.draw_rectangle(self.__bar_x + self.__x, self.__bar_y + self.__y, self.__bar_w, self.__bar_h, self.__bar_border_color)

    def set_range(self, start, end):
        self.__start = start
        self.__end = end
        self.__bar_w = int(self.__current / (self.__end - self.__start) * self.__w * 0.95)
        
    def set_value(self, val):
        ui.clear(self.__x, self.__y, self.__w, self.__h)
        self.__current = val
        self.__bar_w = int(self.__current / (self.__end - self.__start) * self.__w * 0.95)
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

    # create button
    bar = ProgressBar(40, 30, 400, 30)
    bar.set_bg_color((255, 255, 255))
    
    bar.set_value(100)

    clock = time.clock()
    val = 1
    while True:
        clock.tick()
        val +=1
        if val == 100:
            val = 1
        bar.set_value(val)
        ui.display()
        system.parallel_cycle()
        print(clock.fps())