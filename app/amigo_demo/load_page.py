import os
import image
try:
    from ui_canvas import ui
    from ui_label import Label
    from ui_widget import Widget
    from ui_animation import Animation
    from core import system
except:
    from ui.ui_canvas import ui
    from ui.ui_label import Label
    from ui.ui_widget import Widget
    from ui.ui_animation import Animation
    from lib.core import system

import math
class LoadPage:
    def __init__(self):
        self.loop = 0
        ui.set_bg_img(self.create_bg_img())
        setattr(self, "draw_anim", self.draw_anim_)
        system.event(0, self.draw_anim)

    def create_bg_img(self):
        img = image.Image(size=(ui.__w, ui.__h))
        img.draw_rectangle(0, 0, ui.__w, ui.__h, (75, 75, 75), fill=True)
        img.draw_circle(121, 111, int(50),
                            color=(64, 64, 64), thickness=3)  # 10ms
        img.draw_circle(120, 110, int(50),
                            color=(250, 0, 0))  # 10ms
        img.draw_circle(120, 110, int(50), fill=True,
                            color=(250, 0, 0))  # 10ms
        sipeed = b'\x40\xA3\x47\x0F\x18\x38\x18\x0F\x07\x03\x00\x00\x00\x0F\x0F\x0F\x00\xFC\xFC\xFC\x00\x00\x00\xF0\xF8\xFC\x06\x07\x06\xFC\xF8\xF0'
        img.draw_font(88, 80, 16, 16, sipeed, scale=4, color=(64,64,64))
        img.draw_font(86, 78, 16, 16, sipeed, scale=4, color=(255,255,255))
        return img

    
    def draw_anim_(self):
        self.loop+=1
        img = image.Image(size=(250, 100))
        img.draw_rectangle(0, 0, 250, 100, (75, 75, 75), fill=True)
        value = math.cos(math.pi * self.loop / 8) * 4
        if self.loop > 20:
            img.draw_string(6 - int(value) * 2, -2 + (int(value) % 8) * 2, "A",
                                color=(64, 64, 64), scale=8, mono_space=0)
            img.draw_string(6 - int(value), 2 + (int(value) % 8), "A",
                                color=(0x2d, 0x85, 0xf0), scale=8, mono_space=0)
        else:
            img.draw_string(9, 3, "A", color=(
                64, 64, 64), scale=8, mono_space=0)

        if self.loop > 40:
            img.draw_string(9, 2 - int(value) * 5 - 9, "  m",
                                color=(64, 64, 64), scale=8, mono_space=0)
            img.draw_string(9, 0 - int(value) * 4 - 8, "  m",
                                color=(0xf4, 0x43, 0x3c), scale=8, mono_space=0)
        else:
            img.draw_string(9, 2, "  m",
                                color=(64, 64, 64), scale=8, mono_space=0)

        if self.loop > 40:
            img.draw_string(9, 2, "    i",
                                color=(64, 64, 64), scale=8, mono_space=0)
            img.draw_string(6, 0, "    i",
                                color=(0xff, 0xbc, 0x32), scale=8, mono_space=0)

            img.draw_rectangle((110, 7, 12, 12),
                                color=(75, 75, 75), fill=True)

            img.draw_string(65, -26 + int(value), "    .    ",
                                color=(64, 64, 64), scale=4, mono_space=0)
            img.draw_string(62, -28 + int(value), "    .    ",
                                color=(0xff, 0xbc, 0x32), scale=4, mono_space=0)
        else:
            img.draw_string(9, 2, "    i",
                                color=(64, 64, 64), scale=8, mono_space=0)
            img.draw_rectangle((110, 7, 12, 12),
                                color=(75, 75, 75), fill=True)
            img.draw_string(65, -26, "    .    ",
                                color=(64, 64, 64), scale=4, mono_space=0)

        if self.loop > 60:
            img.draw_string(9 + int(value) * 2 + 10, 0, "     g",
                                color=(64, 64, 64), scale=8, mono_space=0)
            img.draw_string(6 + int(value) * 2 + 10, 0, "     g",
                                color=(0x0a + int(value) * 50, 0xa8, 0x58 + int(value) * 50), scale=8, mono_space=0)
        else:
            img.draw_string(9, 2, "     g",
                                color=(64, 64, 64), scale=8, mono_space=0)

        if self.loop > 60:
            img.draw_string(9 - int(value) * 2 + 20, 2, "       o",
                                color=(64, 64, 64), scale=8, mono_space=0)
            img.draw_string(6 - int(value) * 2 + 20, 0, "       o",
                                color=(0xf4, 0x43 + int(value) * 50, 0x3c), scale=8, mono_space=0)
        else:
            img.draw_string(9, 2, "       o",
                                color=(64, 64, 64), scale=8, mono_space=0)
        
        ui.canvas.draw_image(img, 200, 70)
        del img
        
        if self.loop == 100:
            system.remove(self.draw_anim)


if __name__ == '__main__':
    l = LoadPage()

    while True:
        ui.display()
        system.cycle()