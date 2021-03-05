import os
import image
try:
    from ui_canvas import ui
    from ui_widget import Widget
except:
    from ui.ui_canvas import ui
    from ui.ui_widget import Widget


class TextEdit(Widget):

    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h)
        # text
        self._text = ""
        self._text_color = (255, 255, 255)
        self._text_x = 0
        self._text_y = 0
        self._text_scale = 1
        self._text_spacing = 2

    def draw(self):
        super().draw()
        str_w = len(self._text) * self._text_scale * 6  # 6： default char width
        str_h = self._text_scale * 10  # 10: default char height
        if self._text:
            if str_w <= self.__w:
                ui.img.draw_string(self._text_x + self.__x, self._text_y + self.__y,
                                   self._text, scale=self._text_scale, color=self._text_color)
            else:
                # char nums of every line
                str_el = int(self.__w * 0.9 / (6*self._text_scale))
                self._text_x = int(self.__w * 0.05)
                self._text_y = int(self.__w * 0.05)
                # 将可以填满的行数写完
                for index in range(str_w // str_el):
                    if self._text_y + self._text_scale * 10 > self.__h:
                        return
                    ui.img.draw_string(self._text_x + self.__x, self._text_y + self.__y,
                                       self._text[index*str_el:index*str_el +
                                                  str_el], scale=self._text_scale,
                                       color=self._text_color)
                    self._text_y += self._text_scale * 10 + self._text_spacing
                # 写剩余的字数
                self._text_y += self._text_scale * 10 + self._text_spacing
                if self._text_y + self._text_scale * 10 > self.__w * 0.9:
                    return
                ui.img.draw_string(self._text_x + self.__x, self._text_y + self.__y,
                                   self._text[str_w - str_w %
                                              str_el:], scale=self._text_scale,
                                   color=self._text_color)

    def get_text(self):
        return self._text

    def set_text(self, text, color=(255, 255, 255), scale=1, padding_top=None, padding_left=None):
        self._text = text
        self._text_scale = scale

        str_w = len(self._text) * self._text_scale * 6  # 6： default char width
        str_h = self._text_scale * 10  # 10: default char height

        # default pos: align center
        self._text_x = int((self.__w - str_w) / 2)
        self._text_y = int((self.__h - str_h) / 2)

        # char nums of every line
        str_el = int(self.__w * 0.9 / (6*self._text_scale))
        # str lines
        str_lines = int(str_w / str_el)
        str_high = int(str_lines * str_h)

        # custom pos
        if padding_top:
            self._text_x = padding_top
        if padding_left:
            self._text_y = padding_left
        self.clear()
        self.draw()


if __name__ == '__main__':
    try:
        from touch import Touch
        from core import system
    except:
        from driver.touch import Touch
        from lib.core import system
    import time

    # init canvas
    ui.set_bg_color((75, 0, 75))
    ui.set_bg_img("res/images/bg.jpg")

    # create button
    lab = TextEdit(20, 20, 280, 180)
    lab.set_bg_color(None)
    lab.set_border((255, 255, 255), 2)

    system.event(0, ui.display)
    clock = time.clock()
    val = 1
    while True:
        clock.tick()
        lab.set_text(lab.get_text()+"a", scale=2)
        system.parallel_cycle()
        print(clock.fps())
