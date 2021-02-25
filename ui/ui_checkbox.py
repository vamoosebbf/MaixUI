import os
import image
try:
    from ui_button import Button
    from touch import Touch,touch
    from core import system
except:
    from ui.ui_button import Button
    from driver.touch import Touch,touch
    from lib.core import system

class CheckBox(Button):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h)
        self.__rect_color  = (255, 255, 255)
        self.__rect_border_color = (0, 0, 0)
        self.__value = None
        self.__checked = False

    def draw(self, canvas):
        super().draw(canvas)

        w = self._text_scale * 6 * 2 # 正方形选中框的大小为单个 char 的两倍
        img = image.Image(size = (w, w))
        img.draw_rectangle(0, 0, w, w, self.__rect_color, fill = True)
        img.draw_rectangle(0, 0, w, w, self.__rect_border_color)
        x = self.__x + self._text_x - w - 5
        y = self.__y + ((self.__h - img.height()) // 2)
        canvas.draw_img(img, x, y, alpha=255)

    def set_rect_color(self, color):
        self.__rect_color = color
    
    def set_checked(self, checked):
        self.__checked = checked
    
    def get_checked(self):
        return self.__checked

if __name__ == '__main__':
    
    try:
        from ui_canvas import Canvas
    except:
        from ui.ui_canvas import Canvas
    # create button
    checkbox1 = CheckBox(100, 82, 100, 30)
    checkbox1.set_text("apple")
    checkbox1.set_border_color((255, 255, 255))

    def on_press(btn):
        if checkbox1.get_checked():
            checkbox1.set_checked(False)
            checkbox1.set_rect_color((255, 255, 255))
        else:
            checkbox1.set_checked(True)
            checkbox1.set_rect_color((0, 0 ,255))
    
    checkbox1.register_event(Touch.press, on_press)
    ui = Canvas()
    ui.add_widget(checkbox1)
    
    ui.set_bg_color((75, 0, 75))

    while True:
        ui.display()
        system.parallel_cycle()