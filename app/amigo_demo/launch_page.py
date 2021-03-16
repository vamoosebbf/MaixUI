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

class LaunchPage:
    a = b'\x00\x00\x03\x03\x07\x07\x0E\x0E\x1C\x1F\x38\x38\x70\xF0\x00\x00\x00\x00\xC0\xC0\xE0\xE0\x70\x70\x38\xF8\x1C\x1C\x0E\x0F\x00\x00'
    m = b'\x00\x00\x00\x00\x00\x67\x7F\x61\x61\x61\x61\x61\x61\x61\x00\x00\x00\x00\x00\x00\x00\x1C\xFE\x86\x86\x86\x86\x86\x86\x86\x00\x00'
    i = b'\x00\x00\x01\x00\x00\x01\x01\x01\x01\x01\x01\x01\x01\x01\x00\x00\x00\x00\x80\x00\x00\x80\x80\x80\x80\x80\x80\x80\x80\x80\x00\x00'
    g = b'\x00\x00\x00\x00\x00\x07\x1C\x18\x38\x1C\x1F\x30\x1F\x30\x70\x1F\x00\x00\x00\x00\x00\xCE\x72\x30\x38\x70\xC0\x00\xF8\x0C\x0E\xF8'
    o = b'\x00\x00\x00\x00\x00\x03\x1E\x38\x70\x70\x70\x38\x1C\x03\x00\x00\x00\x00\x00\x00\x00\xC0\x78\x1C\x0C\x0E\x0E\x1C\x38\xC0\x00\x00'
    def __init__(self):
        # ui.set_bg_img(self.create_bg_img())
        self.draw()

    def draw(self):

        #ui.canvas.draw_rectangle((0, 0, ui.height, ui.weight),
                                        #fill = True, color = (0, 0, 0))
        #ui.canvas.draw_rectangle((0, 0, ui.height, ui.weight), fill = True, color = (0x70, 0x80, 0x90))
        ui.canvas.draw_rectangle((0, 0, ui.__w, ui.__h), fill = True, color = (215, 228, 181))
        #ui.canvas.draw_rectangle((0, 0, ui.height, ui.weight),
                                        #fill = True, color = (37, 40, 55))
        #ui.canvas.draw_string(203, 73, "Amigo",
                            #color=(64, 64, 64), scale=8, mono_space=0)
        ui.canvas.draw_font(182, 82, 16, 16, LaunchPage.a, scale=5, color=(37, 40, 55))
        ui.canvas.draw_font(180, 80, 16, 16, LaunchPage.a, scale=5, color=(0x2d, 0x85, 0xf0))
        ui.canvas.draw_font(252, 82, 16, 16, LaunchPage.m, scale=4, color=(37, 40, 55))
        ui.canvas.draw_font(250, 80, 16, 16, LaunchPage.m, scale=4, color=(0xf4, 0x43, 0x3c))
        ui.canvas.draw_font(292, 82, 16, 16, LaunchPage.i, scale=4, color=(37, 40, 55))
        ui.canvas.draw_font(290, 80, 16, 16, LaunchPage.i, scale=4, color=(0xff, 0xbc, 0x32))
        ui.canvas.draw_font(332, 77, 16, 16, LaunchPage.g, scale=4, color=(37, 40, 55))
        ui.canvas.draw_font(330, 75, 16, 16, LaunchPage.g, scale=4, color=(0x0a, 0xa8, 0x58))
        ui.canvas.draw_font(392, 82, 16, 16, LaunchPage.o, scale=4, color=(37, 40, 55))
        ui.canvas.draw_font(390, 80, 16, 16, LaunchPage.o, scale=4, color=(0xf4, 0x43, 0x3c))
        #ui.canvas.draw_string(200, 70, "A",
                            #color=(0x2d, 0x85, 0xf0), scale=8, mono_space=0)
        #ui.canvas.draw_string(200, 70, "  m",
                            #color=(0xf4, 0x43, 0x3c), scale=8, mono_space=0)
        #ui.canvas.draw_string(200, 70, "    i",
                            #color=(0xff, 0xbc, 0x32), scale=8, mono_space=0)
        #ui.canvas.draw_string(200, 70, "     g",
                            #color=(0x0a, 0xa8, 0x58), scale=8, mono_space=0)
        #ui.canvas.draw_string(200, 70, "       o",
                            #color=(0xf4, 0x43, 0x3c), scale=8, mono_space=0)

        value = math.cos(math.pi * launcher.alpha / 12) * 50 + 200
        launcher.alpha = (launcher.alpha + 1) % 24

        for pos in range(0, len(launcher.app_sets)):
            checked = (pos == launcher.app_select)
            launcher.app_sets[pos].draw(checked, value if checked else 255)

if __name__ == '__main__':
    l = LaunchPage()

    while True:
        ui.display()
        system.parallel_cycle()