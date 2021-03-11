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
        self.items_list = []
        self.__max_item_p = 0
        self.__item_h = 0
        self.__Item_w = 0

    def add_items(self, wig):
        self.items_list.append(wig)
        self.draw()

    def set_item_size(self, w, h):
        self.__item_w = w
        self.__item_h = h
        self.draw()

    def draw(self):
        super().draw()
        item_x = 0
        item_y = 0
        self.__max_item_p = self.__h//self.__item_h
        for item in self.items_list[0:self.__max_item_p]:
            item.set_pos_size(self.__x + item_x, self.__y +
                              item_y, self.__item_w, self.__item_h)
            item_x += self.__item_w + 4


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
    li.set_item_size(60, 30)

    lab = Label()
    lab.set_text("apple", color=(255, 0, 0), scale=2)
    li.add_items(lab)

    lab1 = Label()
    lab1.set_text("banana", color=(255, 0, 0), scale=2)
    li.add_items(lab1)

    te1 = TextEdit()
    te1.set_text("texttext", color=(0,255,0), scale=2)
    li.add_items(TextEdit)
    while True:
        ui.display()
