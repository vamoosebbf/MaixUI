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
        self.__eves = {Touch.press:None, Touch.click: None, Touch.idle:None}
        self.__eargs = {Touch.press:None, Touch.click: None, Touch.idle:None}
        touch.register_touch_event(self.touch_event, None)

    # 将 widget 显示在 Canvas 上
    def draw(self, canvas):
        pass

    def free(self):
        pass

    def _point_in_widget(self, point):
        x = point[0]
        y = point[1]
        if x > self.__x and x < self.__x + self.__w and y > self.__y and y < self.__y + self.__h:
            return True
        return False
    
    def touch_event(self, *args):
        print(touch.state)
        if self._point_in_widget(touch.points[1]) and self.__eves[touch.state] != None:
            self.__eves[touch.state](self.__eargs[touch.state]) if self.__eargs[touch.state] else self.__eves[touch.state]()
        elif touch.state == Touch.idle:
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
    
    def set_pos(self, x, y):
        self.__x = x
        self.__y = y

if __name__ == '__main__':

    try:
        from ui_canvas import Canvas
        from touch import Touch
        from core import system
    except:
        from ui.ui_canvas import Canvas
        from driver.touch import Touch
        from lib.core import system

    # create button
    btn = Widget(0, 0, 100, 100)
    # register event
    def on_press():
        btn.set_bg_color((0,0,255))
        btn.set_size(100, 100)
        print("btn press")

    def on_release():
        btn.set_bg_color((255, 0, 0))
        btn.set_size(80, 80)
        print("btn idle")
    
    btn.register_event(Touch.click, on_press)
    btn.register_event(Touch.idle, on_release)
    
    ui = Canvas()
    ui.add_widget(btn)
    
    ui.set_bg_color((75, 0, 75))

    while True:
        ui.display()
        system.parallel_cycle()