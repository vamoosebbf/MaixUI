import os
import image
try:
    from ui_canvas import ui
    from ui_widget import Widget
    from ui_label import Label
except:
    from ui.ui_canvas import ui
    from ui.ui_widget import Widget
    from ui.ui_label import Label


class VLayout(Widget):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h)
        self.widgets_list = []
        self.__max_widget_p = 0
        self.__widget_h = 0
        self.__widget_w = 0
        self.__widget_spc = 0
        self.__stretch_all = 0

    def add_widgets(self, wig, stretch_factor = 1):
        self.widgets_list.append([wig, stretch_factor])
        self.__stretch_all += stretch_factor
        self.draw()

    # set widget spacing
    def set_widget_spc(self, spc):
        self.__widget_spc = spc
        if self.__stretch_all == 0:
            return 
        self.draw()

    def draw(self):
        super().draw()
        widget_x = 0
        widget_y = 0
        self.__widget_h = int(self.__h / self.__stretch_all - self.__widget_spc)
        for widget in self.widgets_list:
            widget[0].set_pos_size(self.__x + widget_x, self.__y +
                              widget_y, self.__w, self.__widget_h*widget[1])
            widget_y += self.__widget_h*widget[1] + self.__widget_spc


if __name__ == '__main__':
    try:
        from ui_label import Label
        from core import system
    except:
        from ui.ui_label import Label
        from lib.core import system
    
    ui.set_bg_color((255, 255, 255))
    li = VLayout(10, 10, 200, 200)

    lab = Label()
    lab.set_bg_color((0, 0, 255))
    lab.set_text("apple", color=(255, 0, 0), scale=2)

    lab1 = Label()
    lab1.set_text("banana", color=(255, 0, 0), scale=2)
    lab1.set_bg_color((255, 0, 255))
    li.add_widgets(lab1, 2)
    li.set_widget_spc(1)
    li.add_widgets(lab, 1)

    while True:
        ui.display()
        system.parallel_cycle()