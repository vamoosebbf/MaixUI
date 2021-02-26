import os
import image
try:
    from ui_progress_bar import ProgressBar
except:
    from ui.ui_prgress_bar import ProgressBar

class Slider(ProgressBar):
    def __init__(self):
        super().__init__()
        # handle： 触球
        self.__handle_color = (221, 38, 41)
        self.__handle_w = self.__h
        self.__handle_h = self.__h
        self.__handle_border_color = None
        self.__handle_border_thickness = 1

    def draw(self, canvas):
        super().draw(canvas)
        handle_x = int(self.__bar_w + self.__bar_x - self.__handle_w / 2)
        handle_y = int(self.__y)
        self.__panel.draw_circle(handle_x, handle_y, radius = self.__handle_w // 2, fill = True)
