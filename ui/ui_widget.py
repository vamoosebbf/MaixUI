import image

try:
    from ui_canvas import ui
    from touch import Touch, touch
    from core import system
except ImportError:
    from ui.ui_canvas import ui
    from driver.touch import Touch, touch
    from lib.core import system


class Widget:
    def __init__(self, x, y, w, h):
        self.__x = x
        self.__y = y
        self.__w = w
        self.__h = h

        self.__border_color = None
        self.__border_thickness = 0
        self.__bg_color = None
        self.__bg_img = None
        self.__bg_img_padding_left = None
        self.__bg_img_padding_top = None

        self.__eves = {Touch.press: None, Touch.click: None,
                       Touch.idle: None, Touch.drag: None}
        self.__eargs = {Touch.press: None, Touch.click: None,
                        Touch.idle: None, Touch.drag: None}
        self.__eve_enable = False

    # 将 widget 显示在 Canvas 上
    def draw(self):
        # fill background
        if self.__bg_color:
            ui.img.draw_rectangle(
                self.__x, self.__y, self.__w, self.__h, color=self.__bg_color, fill=True)
        if self.__bg_img:
            ui.img.draw_image(self.__bg_img, self.__x + self.__bg_img_padding_left,
                              self.__y + self.__bg_img_padding_top, alpha=255)
        if self.__border_color:
            ui.img.draw_rectangle(self.__x, self.__y, self.__w, self.__h,
                                  self.__border_color, thickness=self.__border_thickness)

    def _point_in_widget(self, point):
        x = point[0]
        y = point[1]
        if x >= self.__x and x <= self.__x + self.__w and y >= self.__y and y <= self.__y + self.__h:
            return True
        return False

    def touch_event(self, *args):
        if self._point_in_widget(touch.points[1]) and self.__eves[touch.state] != None:
            self.__eves[touch.state](
                self.__eargs[touch.state]) if self.__eargs[touch.state] else self.__eves[touch.state]()

    # eve_name: event name, string type
    def register_event(self, eve_name, func, *args):
        if self.__eve_enable == False:
            touch.register_touch_event(self.touch_event, None)
            self.__eve_enable = True
        for e in self.__eves.keys():
            if e == eve_name:
                self.__eves[e] = func
                self.__eargs[e] = args
                return
        print("event name error, please use follow values:")
        for i in self.__eves.keys():
            print(i)

    def unregister_event(self, eve_name):
        for e in self.__eves.keys():
            if e == eve_name:
                self.__eves[e] = None
                self.__eargs[e] = None
                return
        print("event name error, please use follow values:")
        for i in self.__eves.keys():
            print(i)

    def set_bg_color(self, color):
        self.__bg_color = color
        self.draw()

    def set_bg_img(self, img, padding_left=None, padding_top=None):
        self.__bg_img = img
        w = self.__bg_img.width()
        h = self.__bg_img.height()

        # default center
        self.__bg_img_padding_left = (self.__w - w) // 2
        self.__bg_img_padding_top = (self.__h - h) // 2

        # custom pos
        if padding_left:
            self.__bg_img_padding_left = padding_left
        if padding_top:
            self.__bg_img_padding_top = padding_top
        self.draw()

    # set position and size
    def set_pos_size(self, x, y, w, h):
        self.clear()
        self.__w = w
        self.__h = h
        self.__x = x
        self.__y = y
        if self.__bg_img:
            self.set_bg_img(self.__bg_img.resize(w, h))
        self.draw()

    def set_border(self, color, thickness):
        self.__border_color = color
        self.__border_thickness = thickness
        self.draw()

    # clear background
    def clear(self):
        ui.clear(self.__x - self.__border_thickness, self.__y - self.__border_thickness,
                 self.__w + self.__border_thickness, self.__h + self.__border_thickness)


if __name__ == '__main__':
    import time
    import os
    try:
        from touch import Touch
        from core import system
    except:
        from driver.touch import Touch
        from lib.core import system

    ui.set_bg_color((255, 255, 0))

    img = image.Image(os.getcwd() + "/res/icons/app_camera.bmp")
    print(img)
    # create widget
    wig = Widget(0, 0, 100, 100)
    wig.set_pos_size(0, 0, 80, 80)
    wig.set_bg_img(img)
    wig.set_border((255, 255, 255), 1)

    def on_press():
        wig.set_bg_color((0, 0, 255))
        wig.set_pos_size(0, 0, 100, 100)
        print("wig press")

    def on_idle():
        wig.set_bg_color((255, 0, 0))
        wig.set_pos_size(0, 0, 80, 80)
        print("wig idle")

    def on_drag():
        wig.set_bg_color((255, 0, 0))
        wig.set_pos_size(0, 0, 80, 80)
        print("wig idle")

    wig.register_event(Touch.drag, on_drag)
    system.event(0, ui.display)
    clock = time.clock()
    pos_x = 0
    pos_y = 20
    while True:
        clock.tick()
        pos_x += 2
        wig.set_pos_size(pos_x, pos_y, 80, 80)
        system.parallel_cycle()
        print(clock.fps())
