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
    
    def touch_event(self):
        if self._point_in_widget(touch.points[0]):
            if touch.state == Touch.press and self.__eves[Touch.press] != None:
                self.__eves[Touch.press](self.__eargs[Touch.press]) if self.__eargs[Touch.press] else self.__eves[Touch.press]()
            if touch.state == Touch.release and self.__eves[Touch.release] != None:
                self.__eves[Touch.release](self.__eargs[Touch.release]) if self.__eargs[Touch.release] else self.__eves[Touch.release]()

    # eve_name: event name, string type
    def register_event(self, eve, func, *args):
        touch.register_touch_event(self.touch_event)
        for e in self.__eves.keys():
            if e == eve:
                self.__eves[eve] = func
                self.__eargs[eve] = func
                return       
        print("cvent name error, please use follow values:")
        for i in self.__eves.keys():
            print(i)

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