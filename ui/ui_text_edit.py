import os
import image
try:
    from ui_canvas import ui
    from ui_widget import Widget
    from touch import Touch, touch
except:
    from ui.ui_canvas import ui
    from ui.ui_widget import Widget
    from driver.touch import Touch, touch


class TextEdit(Widget):

    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h)
        # text
        self._text = ""
        self._text_color = (255, 255, 255)
        self._text_x = 0
        self._text_y = 0
        self._text_scale = 1
        self._text_lspacing = 2
        self._text_oft = 0  # text draw offset
        self._max_line_p = 0
        self._padding = self.__w * 0.05
        self.register_event(Touch.drag, self.on_drag)

    def on_drag(self):
        # drag distance in y-axis direction
        dis = touch.points[0][1] - touch.points[1][1]
        str_el = int(self.__w * 0.9 / (6*self._text_scale))
        self._text_oft += int(dis // 6 * str_el)

        if self._text_oft < 0:
            self._text_oft = 0
        elif self._text_oft > self._text_max_oft:
            self._text_oft = self._text_max_oft
        self.clear()
        self.draw()

    def text_draw(self):
        # length of text which will be draw , 6： default char width
        str_len = len(self._text[self._text_oft:])
        str_h = self._text_scale * 10  # 10: default char height

        # char nums of every line
        str_el = int(self.__w * 0.9 / (6*self._text_scale))
        text_x = int(self._padding)
        text_y = int(self._padding)
        # 将可以填满的行数写完
        for index in range(self._max_line_p):
            if text_y + self._text_scale * 10 > self.__h:
                return
            tmp = index * str_el + self._text_oft
            ui.img.draw_string(text_x + self.__x, text_y + self.__y,
                               self._text[tmp:tmp + str_el],
                               scale=self._text_scale,
                               color=self._text_color)
            text_y += self._text_scale * 10 + self._text_lspacing

    def draw(self):
        super().draw()
        if self._text:
            self.text_draw()

    def get_text(self):
        return self._text

    def set_text(self, text, color=(255, 255, 255), scale=1, lspacing=None):
        self._text = text
        self._text_color = color
        self._text_scale = scale
        if lspacing:
            self._text_lspacing = lspacing
        str_len = len(self._text) * self._text_scale * 6
        str_el = int((self.__w * 0.9) / (6*self._text_scale))
        # one page can
        self._max_line_p = int(
            (self.__h - self._padding*2) // (self._text_scale * 10 + self._text_lspacing))
        tmp = len(self._text)/str_el - self._max_line_p
        if tmp < 0:
            tmp = 0
        elif tmp % 1 > 0:
            tmp += 1
        self._text_max_oft = int(tmp) * str_el
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
    lab.set_text("MaixPy is to port Micropython to K210\
                 (a 64-bit dual-core RISC-V CPU with hardware FPU, \
                 convolution accelerator, FFT, Sha256) is a project\
                 that supports the normal operation of the MCU\
                 and integrates hardware acceleration. AI machine\
                 vision and microphone array, 1TOPS computing power\
                 core module is less than ￥50, in order to quickly\
                 develop intelligent applications in the field of AIOT with\
                 extremely low cost and practical size.", scale=2, lspacing=4)
    while True:
        clock.tick()
        system.parallel_cycle()
        # print(clock.fps())
