import os
import image
try:
    from ui_progress_bar import ProgressBar
except:
    from ui.ui_prgress_bar import ProgressBar

class Slider(ProgressBar):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h)
        # handle： 触球
        self.__handle_color = (221, 38, 41)
        self.__handle_w = int(self.__h * 0.9)
        self.__handle_h = int(self.__handle_w)
        self.__handle_border_color = None
        self.__handle_border_thickness = 1

    def draw(self, canvas):
        super().draw(canvas)
        handle_x = int(self.__bar_x + self.__bar_w - self.__handle_h / 2)
        handle_y = int(self.__h * 0.1 / 2)
        self.__panel.draw_rectangle(handle_x, handle_y, self.__handle_w, self.__handle_h, color = self.__handle_color, fill = True)
        canvas.draw_img(self.__panel, self.__x, self.__y)

if __name__ == '__main__':
    
    try:
        from ui_canvas import Canvas
        from core import system
    except:
        from ui.ui_canvas import Canvas
        from lib.core import system

    # create button
    bar = Slider(40, 30, 400, 30)
    bar.set_bg_color((255, 255, 255))
    
    bar.set_value(100)

    ui = Canvas()

    ui.add_widget(bar)
    
    ui.set_bg_color((75, 0, 75))

    while True:
        ui.display()
        system.parallel_cycle()