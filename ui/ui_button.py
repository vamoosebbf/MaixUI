import os
import image
try:
    from ui_widget import Widget
except:
    from ui.ui_widget import Widget

class Button(Widget):
    
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h)
        self.img = None
        # text 
        self._text = ""
        self._text_color = (255, 255, 255)
        self._text_x = 0
        self._text_y = 0
        self._text_scale = 1
        self.__bg_color = None
        self.__bg_img_path = None
        self.__img = None

        self.__bg_img_padding_left = None
        self.__bg_img_padding_top = None
        
        self._border_color = None
            
    def draw(self, canvas):
        self.img = image.Image(size=(self.__w, self.__h))
        if self.__bg_color:
            self.img.draw_rectangle(0, 0, self.__w, self.__h, self.__bg_color, fill = True)
        if self.__bg_img_path:
            self.img = image.Image(self.__bg_img_path).resize(self.__w, self.__h)
        if self._text:
            self.img.draw_string(self._text_x, self._text_y,self._text, scale=self._text_scale, color=self._text_color)
        if self._border_color:
            self.img.draw_rectangle(0, 0, self.__w, self.__h, self._border_color)
        canvas.draw_img(self.img, self.__x, self.__y, alpha=255)

    # align: 0 center, 1 right, 2 left
    def set_text(self, text, color=(255, 255, 255), scale = 1, padding_top = None, padding_left = None):
        self._text = text
        self._text_scale = scale

        # default pos: align center
        str_w = len(self._text) * self._text_scale * 6 # 6： default char width
        str_h = self._text_scale * 10 # 10: default char height
        self._text_x = (self.__w - str_w) // 2
        self._text_y = (self.__h - str_h) // 2

        # custom pos
        if padding_top:
            self._text_x = padding_top
        if padding_left:
            self._text_y = padding_left

    def set_border_color(self, border_color):
        self._border_color = border_color

if __name__ == '__main__':
    try:
        from ui_canvas import Canvas
    except:
        from ui.ui_canvas import Canvas

    # create button
    btn = Button(0, 0, 80, 80)
    btn.set_text("aaa", scale = 2)
    btn.set_text("bbb", scale = 2)
    btn.set_bg_img(path = os.getcwd() + "/res/icons/app_camera.bmp")
    btn.set_bg_color((255, 0, 0))
    # register event
    def on_press(self):
        btn.set_bg_color((0,0,255))
        btn.set_size(100, 100)
        print("btn press")

    def on_release(self):
        btn.set_bg_color((255, 0, 0))
        btn.set_size(80, 80)
        print("btn release")
    
    btn.register_event(Touch.click, on_press)
    btn.register_event(Touch.idle, on_release)
    
    # create button
    btn2 = Button(400, 82, 80, 80)
    btn.set_border_color((255, 255, 255))
    btn2.set_text("apple")

    # create button
    btn3 = Button(400, 164, 80, 80)
    btn3.set_bg_img(os.getcwd() + "/res/icons/app_explorer.bmp")

    # create button
    btn4 = Button(400, 246, 80, 80)
    btn4.set_bg_img(os.getcwd() + "/res/icons/app_system_info.bmp")
    
    ui = Canvas()
    ui.add_widget(btn)
    ui.add_widget(btn2)
    ui.add_widget(btn3)
    ui.add_widget(btn4)
    
    ui.remove_widget(btn4)
    
    ui.set_bg_color((75, 0, 75))

    while True:
        ui.display()
        system.parallel_cycle()