import os
import image
try:
    from ui_canvas import ui
    from ui_widget import Widget
except:
    from ui.ui_canvas import ui
    from ui.ui_widget import Widget


class Label(Widget):

    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h)
        # text
        self._text = ""
        self._text_color = (255, 255, 255)
        self._text_x = 0
        self._text_y = 0
        self._text_scale = 1

    def draw(self):
        super().draw()
        if self._text:
            ui.img.draw_string(self._text_x + self.__x, self._text_y + self.__y,
                               self._text, scale=self._text_scale, color=self._text_color)

    # align: 0 center, 1 right, 2 left
    def set_text(self, text, color=(255, 255, 255), scale=1, padding_top=None, padding_left=None):
        self._text = text
        self._text_scale = scale
        self._text_color = color
        # default pos: align center
        str_w = len(self._text) * self._text_scale * 6  # 6： default char width
        str_h = self._text_scale * 10  # 10: default char height
        # The character width is larger than the Widget width, discard the excess
        if str_w > self.__w:
            text_max_num = self.__w // (self._text_scale * 6)
            self._text = self._text[0:text_max_num]
            str_w = text_max_num * (self._text_scale * 6)
        # test start point
        self._text_x = int((self.__w - str_w) / 2)
        self._text_y = int((self.__h - str_h) / 2)

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

    # create button
    lab = Label(10, 10, 80, 80)
    lab.set_bg_color((255, 0, 0))
    lab.set_text("bbb", scale=2)
    lab.set_border((255, 255, 255), 2)

    system.event(0, ui.display)
    clock = time.clock()
    val = 1
    while True:
        clock.tick()
        val += 1
        lab.set_text(str(val), scale=2)
        system.parallel_cycle()
        print(clock.fps())
