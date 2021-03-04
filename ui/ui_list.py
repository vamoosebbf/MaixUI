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


class List(Widget):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h)
        self.items_list = []

    def add_items(self, text):
        lab = Label(current_x, current_y, self.__w, self.__h/(len(self.items_list))
        self.items_list.append(lab)

    def draw(self):
        super().draw()
        for item in self.items_list:
            item.draw()


if __name__ == '__main__':
    li=List(10, 10, 200, 300)
