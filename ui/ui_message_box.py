import os
import image
try:
    from ui_canvas import ui
    from touch import Touch, touch
    from ui_widget import Widget
    from ui_label import Label
    from ui_button import Button
except:
    from ui.ui_canvas import ui
    from driver.touch import Touch, touch
    from ui.ui_widget import Widget
    from ui.ui_label import Label
    from ui.ui_button import Button


class MessageBox(Widget):
    YES = "YES"
    NO = "NO"

    def __init__(self, x, y, w, h, text):
        super().__init__(x, y, w, h)

        self.lab = Label(self.__x, self.__y, self.__w, int(self.__h*2/3))
        self.lab.set_text(text)

        self.btn_yes = Button(self.__x, int(self.__y*5/3),
                              int(self.__x/3), int(self.__y/3))
        self.btn_no = Button(
            int(self.__x + self.btn_yes.__w*1.2), int(self.__y*5/3),
            int(self.__x/3), int(self.__y/3))

        self.set_bg_color((255, 200, 0))
        self.btn_yes.set_text(self.YES)

        self.set_bg_color((255, 200, 0))
        self.btn_no.set_text(self.NO)

    def draw(self):
        super().draw()
        self.lab.draw()
        self.btn_yes.draw()
        self.btn_no.draw()


if __name__ == '__main__':
    from core import system

    ui.set_bg_color((255, 255, 255))

    btn = Label(10, 10, 60, 40)
    btn.set_text("click me", scale=1)
    btn.set_bg_color((0, 200, 255))

    def on_click():

        meb = MessageBox(50, 50, 200, 200, "messagebox!!!")
    btn.register_event(Touch.click, on_click)
    system.event(0, ui.display)

    while True:
        system.parallel_cycle()
