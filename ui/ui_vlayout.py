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

    def add_widgets(self, wig):
        self.widgets_list.append(wig)
        self.draw()

    def set_widget_size(self, w, h):
        self.__widget_w = w
        self.__widget_h = h
        self.draw()

    def set_widget_spc(self, spc):
        self._widget_spc = spc
        self.draw()

    def draw(self):
        super().draw()
        widget_x = 0
        widget_y = 0
        self.__max_widget_p = self.__h//self.__widget_h
        for widget in self.widgets_list[0:self.__max_widget_p]:
            widget.set_pos_size(self.__x + widget_x, self.__y +
                              widget_y, self.__widget_w, self.__widget_h)
            widget_y += self.__widget_h + self._widget_spc


if __name__ == '__main__':
    try:
        from ui_label import Label
    except:
        from ui.ui_label import Label
    
    ui.set_bg_color((255, 255, 255))
    li = VLayout(10, 10, 200, 300)
    li.set_widget_size(80, 40)
    li.set_widget_spc(10)

    lab = Label()
    lab.set_bg_color(None)
    lab.set_text("apple", color=(255, 0, 0), scale=2)
    li.add_widgets(lab)

    lab1 = Label()
    lab1.set_text("banana", color=(255, 0, 0), scale=2)
    li.add_widgets(lab1)

    while True:
        ui.display()
