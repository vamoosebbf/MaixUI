import os
import image
try:
    from ui_canvas import ui
    from ui_widget import Widget
    from ui_label import Label
    from ui_button import Button
    from ui_vlayout import VLayout
    from ui_hlayout import HLayout

    from core import system

    from touch import Touch
except:
    from ui.ui_canvas import ui
    from ui.ui_widget import Widget
    from ui.ui_label import Label
    from ui.ui_button import Button
    from ui.ui_vlayout import VLayout
    from ui.ui_hlayout import HLayout

    from lib.core import system

    from driver.touch import Touch

class LaunchPage:
    def __init__(self):
        ui.set_bg_img(self.create_bg_img())
        self.draw_bar()

    def create_bg_img(self):
        a = b'\x00\x00\x03\x03\x07\x07\x0E\x0E\x1C\x1F\x38\x38\x70\xF0\x00\x00\x00\x00\xC0\xC0\xE0\xE0\x70\x70\x38\xF8\x1C\x1C\x0E\x0F\x00\x00'
        m = b'\x00\x00\x00\x00\x00\x67\x7F\x61\x61\x61\x61\x61\x61\x61\x00\x00\x00\x00\x00\x00\x00\x1C\xFE\x86\x86\x86\x86\x86\x86\x86\x00\x00'
        i = b'\x00\x00\x01\x00\x00\x01\x01\x01\x01\x01\x01\x01\x01\x01\x00\x00\x00\x00\x80\x00\x00\x80\x80\x80\x80\x80\x80\x80\x80\x80\x00\x00'
        g = b'\x00\x00\x00\x00\x00\x07\x1C\x18\x38\x1C\x1F\x30\x1F\x30\x70\x1F\x00\x00\x00\x00\x00\xCE\x72\x30\x38\x70\xC0\x00\xF8\x0C\x0E\xF8'
        o = b'\x00\x00\x00\x00\x00\x03\x1E\x38\x70\x70\x70\x38\x1C\x03\x00\x00\x00\x00\x00\x00\x00\xC0\x78\x1C\x0C\x0E\x0E\x1C\x38\xC0\x00\x00'
        img = image.Image(size=(ui.__w, ui.__h))
        img.draw_rectangle((0, 0, ui.__w, ui.__h), fill = True, color = (215, 228, 181))

        img.draw_circle(121, 111, int(50),
                                color=(64, 64, 64), thickness=3)  # 10ms
        img.draw_circle(120, 110, int(50),
                            color=(250, 0, 0))  # 10ms
        img.draw_circle(120, 110, int(50), fill=True,
                            color=(250, 0, 0))  # 10ms

        sipeed = b'\x40\xA3\x47\x0F\x18\x38\x18\x0F\x07\x03\x00\x00\x00\x0F\x0F\x0F\x00\xFC\xFC\xFC\x00\x00\x00\xF0\xF8\xFC\x06\x07\x06\xFC\xF8\xF0'

        img.draw_font(88, 80, 16, 16, sipeed, scale=4, color=(64,64,64))

        img.draw_font(86, 78, 16, 16, sipeed, scale=4, color=(255,255,255))

        img.draw_font(182, 82, 16, 16, a, scale=5, color=(37, 40, 55))
        img.draw_font(180, 80, 16, 16, a, scale=5, color=(0x2d, 0x85, 0xf0))
        img.draw_font(252, 82, 16, 16, m, scale=4, color=(37, 40, 55))
        img.draw_font(250, 80, 16, 16, m, scale=4, color=(0xf4, 0x43, 0x3c))
        img.draw_font(292, 82, 16, 16, i, scale=4, color=(37, 40, 55))
        img.draw_font(290, 80, 16, 16, i, scale=4, color=(0xff, 0xbc, 0x32))
        img.draw_font(332, 77, 16, 16, g, scale=4, color=(37, 40, 55))
        img.draw_font(330, 75, 16, 16, g, scale=4, color=(0x0a, 0xa8, 0x58))
        img.draw_font(392, 82, 16, 16, o, scale=4, color=(37, 40, 55))
        img.draw_font(390, 80, 16, 16, o, scale=4, color=(0xf4, 0x43, 0x3c))
        return img
    
    def draw_bar(self):
        # photo
        #btn
        photo_btn = Button(0,0,64, 64)
        img = image.Image(size=(64, 64))
        tmp1 = b"\x3F\x60\xC0\x80\x80\x80\x80\x90\xB8\xEC\xC6\x83\x81\xC0\x60\x3F\xFC\x06\x3B\x6D\x45\x6D\x39\x01\x01\x41\xE1\xB1\x19\x0F\x06\xFC"
        tmp2 = b"\x00\x00\x00\x00\x00\x00\x00\x10\x38\x6C\x46\x03\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x40\xE0\xB0\x18\x0E\x00\x00"
        tmp3 = b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x38\x6C\x44\x6C\x38\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        img.draw_font(1, 1, 16, 16, tmp1,
                            scale=4, color=(64, 64, 64))
        img.draw_font(0, 0, 16, 16,tmp1,
                            scale=4, color=(255, 165, 0))
        img.draw_font(0, 0, 16, 16, tmp2,
                            scale=4, color=(0x0a, 0xa8, 0x58))
        img.draw_font(0, 0, 16, 16, tmp3,
                            scale=4, color=(230, 69, 0))
        photo_btn.set_bg_img(img)
        # label
        photo_lab = Label(0, 0, 64, 30)
        photo_lab.set_text("Photo",color=(105, 105, 105), scale=2)

        photo_vlay = VLayout(40, 200, 64, 100) 
        photo_vlay.add_widgets(photo_btn,2)
        photo_vlay.add_widgets(photo_lab,1)
        # event
        def btn_on_press(args):
            btn = args[0]
            btn.set_border((255, 255, 255), 2)
        photo_btn.register_event(Touch.press, btn_on_press, photo_btn)
        
        # Demo
        demo_vlay = VLayout(40, 200, 64, 100)
        # button
        tmp1 = b"\x00\x7F\x40\x40\x7F\x40\x40\x48\x50\x61\x53\x4A\x40\x40\x7F\x00\x00\xFE\x02\x02\xFE\x02\x02\x52\xCA\x86\x0A\x12\x02\x02\xFE\x00"
        tmp2 = b"\x00\x7F\x40\x40\x7F\x40\x40\x40\x40\x40\x40\x40\x40\x40\x7F\x00\x00\xFE\x02\x02\xFE\x02\x02\x02\x02\x02\x02\x02\x02\x02\xFE\x00"
        demo_btn = Button(0,0,70, 70)
        img.clear()
        img.draw_font(1, 1, 16, 16, tmp1,
                            scale=4, color=(64, 64, 64))
        img.draw_font(0, 0, 16, 16, tmp1, scale=4,
                            color=(84, 255, 159))
        img.draw_font(0, 0, 16, 16, tmp2, scale=4,
                            color=(47, 79, 79))
        demo_btn.set_bg_img(img)
        # label
        demo_lab = Label(0, 0, 64, 30)
        demo_lab.set_text("Demo", color=(105, 105, 105), scale=2)
        demo_vlay.add_widgets(demo_btn,2)
        demo_vlay.add_widgets(demo_lab,1)
        #event
        demo_btn.register_event(Touch.press, btn_on_press, demo_btn)

        
        # System
        system_vlay = VLayout(40, 200, 64, 100)
        # button
        tmp1 = b"\x00\x03\x19\x3B\x3F\x0E\x5C\x78\x78\x5C\x0E\x3F\x3B\x19\x03\x00\x00\xC0\x98\xDC\xFC\x70\x3A\x1E\x1E\x3A\x70\xFC\xDC\x98\xC0\x00"
        tmp2 = b"\x00\x00\x00\x03\x0F\x0E\x1C\x18\x18\x1C\x0E\x0F\x03\x00\x00\x00\x00\x00\x00\xC0\xF0\x70\x38\x18\x18\x38\x70\xF0\xC0\x00\x00\x00"
        system_btn = Button(0,0,64, 64)
        img.clear()
        img.draw_font(2, 2, 16, 16, tmp1,
                            scale=4, color=(64, 64, 64))
        img.draw_font(0, 0, 16, 16, tmp1, scale=4,
                            color=(193, 205, 193))
        img.draw_font(0, 0, 16, 16, tmp2, scale=4,
                            color=(255, 255, 255))
        system_btn.set_bg_img(img)
        # label
        system_lab = Label(0, 0, 64, 30)
        system_lab.set_text("System", color=(105, 105, 105), scale=2)
        system_vlay.add_widgets(system_btn,2)
        system_vlay.add_widgets(system_lab,1)
        #event
        system_btn.register_event(Touch.press, btn_on_press, system_btn)
        
        # Camera
        camera_vlay = VLayout(0, 0, 90, 100)
        # button
        tmp1 = b"\x00\x3E\x22\x7F\xFF\xC0\xC7\xCF\xDC\xD8\xDC\xCF\xC7\xC0\xFF\x7F\x00\x00\x00\xFE\xFF\x03\x9B\xC3\xE3\x63\xE3\xC3\x83\x03\xFF\xFE"
        tmp2 = b"\x00\x00\x00\x00\x00\x00\x07\x0F\x1C\x18\x1C\x0F\x07\x00\x00\x00\x00\x00\x00\x00\x00\x00\x98\xC0\xE0\x60\xE0\xC0\x80\x00\x00\x00"
        camera_btn = Button(0,0,64, 64)
        img.clear()
        img.draw_font(0, 0, 16, 16, tmp1,
                            scale=4, color=(255, 255, 255))
        img.draw_font(0, 0, 16, 16, tmp2,
                            scale=4, color=(93, 116, 93))
        camera_btn.set_bg_img(img)
        # label
        camera_lab = Label(0, 0, 70, 30)
        camera_lab.set_text("Camera", color=(105, 105, 105), scale=2)
        camera_vlay.add_widgets(camera_btn,2)
        camera_vlay.add_widgets(camera_lab,1)
        #event
        camera_btn.register_event(Touch.press, btn_on_press, camera_btn)

        bar_hlay = HLayout(60, 200, 460, 100)
        bar_hlay.set_widget_spc(40)
        bar_hlay.add_widgets(photo_vlay)
        bar_hlay.add_widgets(demo_vlay)
        bar_hlay.add_widgets(system_vlay)
        bar_hlay.add_widgets(camera_vlay)
        bar_hlay.set_border((255, 0, 0), 1)


if __name__ == '__main__':
    l = LaunchPage()


    while True:
        ui.display()
        system.parallel_cycle()