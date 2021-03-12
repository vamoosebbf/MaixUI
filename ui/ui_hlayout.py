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


class HLayout(Widget):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h)
        self.widgets_list = []
        self.__max_widget = 0
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
        self.__widget_spc = spc
        self.draw()

    def draw(self):
        super().draw()
        widget_x = 0
        widget_y = 0
        self.__max_widget = self.__w//(self.__widget_w + self.__widget_spc)
        for widget in self.widgets_list[0:self.__max_widget]:
            widget.set_pos_size(self.__x + widget_x, self.__y + widget_y, self.__widget_w, self.__widget_h)
            widget_x += self.__widget_w + self.__widget_spc


if __name__ == '__main__':
    try:
        from ui_label import Label
        from ui_text_edit import TextEdit
    except:
        from ui.ui_label import Label
        from ui.ui_text_edit import TextEdit

    img = image.Image("res/images/bg.jpg")
    ui.set_bg_img(img)
    
    li = HLayout(10, 10, 200, 300)
    li.set_widget_size(100, 30)

    lab = Label()
    lab.set_text("apple", color=(255, 0, 0), scale=2)
    lab.set_border((255, 255, 0), 2)
    li.add_widgets(lab)

    lab1 = Label()
    lab1.set_text("banana", color=(255, 0, 0), scale=2)
    lab1.set_border((255, 0, 255), 2)
    li.add_widgets(lab1)

    te1 = TextEdit()
    te1.set_text("text", color=(0,255,0), scale=2)
    te1.set_border((255, 0, 255), 2)
    li.add_widgets(te1)

    te2 = TextEdit()
    te2.set_text("text2", color=(0,255,0), scale=2)
    te2.set_border((255, 0, 255), 2) 
    li.add_widgets(te2)

    while True:
        ui.display()
