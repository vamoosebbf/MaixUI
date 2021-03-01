import os
import image
try:
    from ui_progress_bar import ProgressBar
    from ui_canvas import ui
    from core import system
except:
    from ui.ui_prgress_bar import ProgressBar
    from ui.ui_canvas import ui
    from lib.core import system

class Slider(ProgressBar):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h)
        # handle： 触球
        self.__handle_color = (221, 38, 41)
        self.__handle_w = int(self.__h * 0.7)
        self.__handle_h = int(self.__handle_w)
        self.__handle_border_color = None
        self.__handle_border_thickness = 1

    def draw(self):
        super().draw()
        handle_x = int(self.__bar_x + self.__bar_w - self.__handle_h / 2)
        handle_y = int(self.__h * 0.15)
        ui.img.draw_rectangle(handle_x + self.__x, handle_y + self.__y, self.__handle_w, self.__handle_h, color = self.__handle_color, fill = True)

if __name__ == '__main__':
    
    import time
    from ui_label import Label
    ui.set_bg_color((75, 0, 75))

    # create button
    bar = Slider(20, 30, 400, 30)
    bar.set_bg_color((255, 255, 255))
    
    bar.set_value(100)
    
    lab = Label(440, 30, 30, 30)
    
    clock = time.clock()
    val = 1
    dir = True
    while True:
        clock.tick()
        if dir:
            val +=1
        else:
            val -=1
        if val == 100:
            dir = False
        if val == 0:
            dir = True
        bar.set_value(val)
        lab.set_text(str(bar.__current) + "%")
        ui.display()
        system.parallel_cycle()
        print(clock.fps())