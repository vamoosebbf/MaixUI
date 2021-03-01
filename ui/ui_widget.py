import image

try:
    from ui_canvas import Canvas
    from touch import Touch,touch
    from core import system
except ImportError:
    from ui.ui_canvas import Canvas
    from driver.touch import Touch,touch
    from lib.core import system
class Widget:
    def __init__(self, x, y, w, h):
        self.__x = x
        self.__y = y
        self.__w = w
        self.__h = h
        self.__bg_color = None
        self.__panel = image.Image(size = (self.__w, self.__h))
        
        self.__eves = {Touch.press:None, Touch.click: None, Touch.idle:None}
        self.__eargs = {Touch.press:None, Touch.click: None, Touch.idle:None}
        touch.register_touch_event(self.touch_event, None)

    # 将 widget 显示在 Canvas 上
    def draw(self, canvas):
        self.__panel.clear()
        # fill background
        if self.__bg_color:
            self.__panel.draw_rectangle(0, 0, self.__w, self.__h, color=self.__bg_color, fill = True)
        canvas.draw_img(self.__panel, self.__x, self.__y, alpha=255)

    def free(self):
        pass

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

    def set_bg_img(self, path, padding_left = None, padding_top = None):
        self.__bg_img_path = path
        img = image.Image(self.__bg_img_path)
        w = img.width()
        h = img.height()
        del img
        
        # default center
        self.__bg_img_padding_left = (self.__w - w) // 2
        self.__bg_img_padding_top = (self.__h - h) // 2

        # custom pos
        if padding_left:
            self.__bg_img_padding_left = padding_left
        if padding_top:
            self.__bg_img_padding_top = padding_top

    def set_size(self, w, h):
        self.__w = w
        self.__h = h
        self.__panel = self.__panel.resize(w, h)
    
    def set_pos(self, x, y):
        self.__x = x
        self.__y = y

if __name__ == '__main__':
    import time
    try:
        from ui_canvas import Canvas
        from touch import Touch
        from core import system
    except:
        from ui.ui_canvas import Canvas
        from driver.touch import Touch
        from lib.core import system

    # create widget
    btn = Widget(0, 0, 100, 100)
    btn.set_bg_color((255, 255, 255))
    # register event
    def on_press():
        btn.set_bg_color((0,0,255))
        btn.set_size(100, 100)
        print("wig press")

    def on_idle():
        btn.set_bg_color((255, 0, 0))
        btn.set_size(80, 80)
        print("wig idle")
    
    btn.register_event(Touch.press, on_press)
    btn.register_event(Touch.idle, on_idle)
    
    ui = Canvas()
    ui.add_widget(btn)
    
    ui.set_bg_color((75, 0, 75))

    clock = time.clock()
    while True:
        clock.tick()
        ui.display()
        system.parallel_cycle()
        print(clock.fps())