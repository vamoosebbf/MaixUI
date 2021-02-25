import os
import image

try:
    from ui_widget import Widget
    from touch import Touch,touch
    from core import system
except ImportError:
    from ui.ui_widget import Widget
    from driver.touch import touch
    from lib.core import system

class ImageBox(Widget):
    def __init__(self, x, y, w, h):
        Widget.__init__(self, x, y, w, h)
        self.__panel = image.Image(size = (self.__w, self.__h))
        self._bg_color = (255, 255, 255)
        
        # title text
        self.__title = ""
        self.__title_scale = 1
        self.__title_x = 0
        self.__title_y = 0
        self.__title_color = (255, 255, 255)

    def set_image(self, img, padding_left = None, padding_top = None):
        w = img.width()
        h = img.height()
        x = (self.__w - w) // 2
        y = (self.__h - h) // 2
        if padding_left:
            x = padding_left
        if padding_top:
            y = padding_top
        if self._bg_color:
            self.__panel.draw_rectangle(0, 0, self.__w, self.__h, self._bg_color, fill = True)
        self.__panel.draw_image(img, x, y)

    def set_title(self, title, color = (255, 255, 255), scale = 1, padding_left = None, padding_top= 5):
        self.__title = title
        self.__title_scale = scale
        self.__title_color = color
        tw = len(title) * 6 * self.__title_scale
        th = len(title) * 10
        self.__title_x = (self.__w - tw) // 2
        if padding_left:
            self.__title_x = padding_left
        if padding_top:
            self.__title_y = padding_top

    def set_bg_color(self, color):
        self._bg_color = color

    def draw(self, canvas):
        self.__panel.draw_string(self.__title_x, self.__title_y, self.__title, self.__title_color, scale=self.__title_scale)
        canvas.draw_img(self.__panel, self.__x, self.__y)

if __name__ == '__main__':

    import sensor

    try:
        from ui_canvas import Canvas
    except:
        from ui.ui_canvas import Canvas

    ui = Canvas()

    sensor.reset()                   
                                        
    sensor.set_pixformat(sensor.RGB565) 
    sensor.set_framesize(sensor.QVGA)   
    sensor.skip_frames(time = 2000)     
    
    box = ImageBox(10, 10, 300, 300)
    box.set_title("sensor image", (0, 0, 0), 2)
    ui.add_widget(box)
    
    while(True):
        img = sensor.snapshot()              
        box.set_image(img)
        ui.display()