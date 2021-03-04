import os
import image
try:
    from ui_canvas import ui
    from ui_button import Button
    from touch import Touch, touch
    from core import system
except:
    from ui.ui_canvas import ui
    from ui.ui_button import Button
    from driver.touch import Touch, touch
    from lib.core import system


class CheckBox(Button):
    def __init__(self, x, y, w, h, text):
        super().__init__(x, y, w, h)
        self.__rect_color = (255, 255, 255)
        self.__rect_border_color = (0, 0, 0)

        self.__value = None
        self.__checked = False
        self.set_text(text)
        self.draw()

    def draw(self):
        super().draw()

        handle_w = self._text_scale * 6 * 2  # 正方形选中框的大小为单个 char 的两倍
        x = self.__x + self._text_x - handle_w - 5
        y = self.__y + int((self.__h - handle_w) / 2)
        ui.img.draw_rectangle(x, y, handle_w, handle_w,
                              self.__rect_color, fill=True)
        ui.img.draw_rectangle(x, y, handle_w, handle_w,
                              self.__rect_border_color)

    def set_rect_color(self, color):
        self.clear()
        self.__rect_color = color
        self.draw()

    def set_checked(self, checked):
        self.clear()
        self.__checked = checked
        self.draw()

    def get_checked(self):
        return self.__checked


if __name__ == '__main__':

    # init ui
    ui.set_bg_color((75, 0, 75))

    # create button
    checkbox1 = CheckBox(100, 82, 100, 30, "apple")
    checkbox1.set_text("apple")
    checkbox1.set_border((255, 255, 255), 1)

    def on_press():
        if checkbox1.get_checked():
            checkbox1.set_checked(False)
            checkbox1.set_rect_color((255, 255, 255))
            checkbox1.set_text("banana")
        else:
            checkbox1.set_checked(True)
            checkbox1.set_rect_color((0, 0, 255))
            checkbox1.set_text("apple")

    checkbox1.register_event(Touch.click, on_press)

    while True:
        ui.display()
        system.parallel_cycle()
