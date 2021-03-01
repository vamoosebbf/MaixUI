import image

try:
    from ui_canvas import ui
    from touch import Touch,touch
    from core import system
except ImportError:
    from ui.ui_canvas import ui
    from driver.touch import Touch,touch
    from lib.core import system

class Widget:
    def __init__(self, x, y, w, h):
        self.__x = x
        self.__y = y
        self.__w = w
        self.__h = h

        self.__bg_color = None
        self.__bg_img = None
        self.__bg_img_padding_left = None
        self.__bg_img_padding_top = None

        self.__eves = {Touch.press:None, Touch.click: None, Touch.idle:None}
        self.__eargs = {Touch.press:None, Touch.click: None, Touch.idle:None}
        touch.register_touch_event(self.touch_event, None)

    # 将 widget 显示在 Canvas 上
    def draw(self):
        # fill background
        if self.__bg_color:
            ui.img.draw_rectangle(self.__x, self.__y, self.__w, self.__h, color=self.__bg_color, fill = True)
        if self.__bg_img:
            ui.img.draw_image(self.__bg_img, self.__x + self.__bg_img_padding_left, self.__y + self.__bg_img_padding_top, alpha=255)
        
            
    def _point_in_widget(self, point):
        x = point[0]
        y = point[1]
        if x >= self.__x and x <= self.__x + self.__w and y >= self.__y and y <= self.__y + self.__h:
            return True
        return False
    
    def touch_event(self, *args):
        if self._point_in_widget(touch.points[1]) and self.__eves[touch.state] != None:
            self.__eves[touch.state](self.__eargs[touch.state]) if self.__eargs[touch.state] else self.__eves[touch.state]()

    # eve_name: event name, string type
    def register_event(self, eve_name, func, *args):
        for e in self.__eves.keys():
            if e == eve_name:
                self.__eves[e] = func
                self.__eargs[e] = args
        return       
        print("cvent name error, please use follow values:")
        for i in self.__eves.keys():
            print(i)

    def unregister_event(self, eve_name):
        self.__eves[eve_name] = None
        self.__eargs[eve_name] = None

    def set_bg_color(self, color):
        self.__bg_color = color
        self.draw()

    def set_bg_img(self, path, padding_left = None, padding_top = None):
        self.__bg_img = image.Image(path)
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

    def set_pos_size(self, x, y, w, h):
        ui.clear(self.__x, self.__y, self.__w, self.__h)
        self.__w = w
        self.__h = h
        self.__x = x
        self.__y = y

        self.draw()

if __name__ == '__main__':
    import time, os
    try:
        from touch import Touch
        from core import system
    except:
        from driver.touch import Touch
        from lib.core import system

    ui.set_bg_color((255, 255, 0))

    # create widget
    wig = Widget(0, 0, 100, 100)
    wig.set_pos_size(0, 0, 80, 80)
    wig.set_bg_img(path = os.getcwd() + "/res/icons/app_camera.bmp")

    # register event
    def on_press():
        wig.set_bg_color((0,0,255))
        wig.set_pos_size(0, 0, 100, 100)
        print("wig press")

    def on_idle():
        wig.set_bg_color((255, 0, 0))
        wig.set_pos_size(0, 0, 80, 80)
        print("wig idle")
    
    wig.register_event(Touch.press, on_press)
    wig.register_event(Touch.idle, on_idle)
    
    clock = time.clock()
    pos_x = 0
    pos_y = 20
    while True:
        clock.tick()
        pos_x +=2
        wig.set_pos_size(pos_x, pos_y, 80, 80)
        ui.display()
        system.parallel_cycle()
        print(clock.fps())