import os
import image
try:
    from ui_canvas import ui
    from ui_widget import Widget
    from core import system
    from touch import Touch
except:
    from ui.ui_canvas import ui
    from ui.ui_widget import Widget
    from lib.core import system
    from driver.touch import Touch


class Switch(Widget):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h)
        self.__border_color = (165, 165, 165)
        self.__bg_color = (255, 255, 255)
        self.__handle_color = (165, 165, 165)

        # 开关方块相对位置
        self.__handle_x = 0
        self.__handle_y = 0

        # 文字
        self.__text = "OFF"
        self.__text_x = int(
            (self.__w / 2 - len(self.__text) * 6) / 2 + self.__w / 2)
        self.__text_y = int((self.__h - 10) / 2)

        self.__state = False  # 当前开关状态

        # 注册单击事件
        self.register_event(Touch.click, self.on_click)
        # 显示
        self.draw()

    def on_click(self):
        self.set_state(not self.__state)

    def draw(self):
        super().draw()
        ui.img.draw_rectangle(self.__handle_x + self.__x, self.__handle_y +
                              self.__y, int(self.__w / 2), self.__h, self.__handle_color, fill=True)
        ui.img.draw_string(self.__text_x + self.__x, self.__text_y +
                           self.__y, self.__text, self.__handle_color)

    def set_state(self, state):
        self.clear()
        self.__state = state
        if self.__state == True:
            self.__border_color = (0, 255, 200)
            self.__handle_color = (0, 255, 200)
            self.__handle_x = int(self.__w / 2)
            self.__text = "ON"
            self.__text_x = int((self.__w / 2 - len(self.__text) * 6) / 2)
        else:
            self.__border_color = (165, 165, 165)
            self.__handle_color = (165, 165, 165)
            self.__handle_x = 0
            self.__text = "OFF"
            self.__text_x = int(
                (self.__w / 2 - len(self.__text) * 6) / 2 + self.__w / 2)
        self.draw()

    def get_state(self):
        return self.__state


if __name__ == '__main__':

    import time
    from ui_label import Label

    # init canvas
    ui.set_bg_color((75, 0, 75))

    # create button
    swi = Switch(20, 30, 60, 40)

    system.event(0, ui.display)
    clock = time.clock()
    while True:
        clock.tick()
        system.parallel_cycle()
        print(clock.fps())
