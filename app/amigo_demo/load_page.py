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

class LoadPage:
    def __init__(self):
        ui.set_bg_img(self.create_bg_img())
        self.draw_anim()

    def create_bg_img(self):
        img = image.Image(size=(ui.__w, ui.__h))
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

    
    def draw_anim(self):
        text_start = 203

        text_x_A = text_start
        la_A = Label(text_x_A, 73, 8*6, 10*8)
        la_A.set_text("A", color=(64, 64, 64), scale=8)

        text_x_A2 = text_start
        la_A2 = Label(text_x_A+5, 70, 8*6, 10*8)
        la_A2.set_text("A", color=(0x2d, 0x85, 0xf0), scale=8)

        text_start += 8*6
        text_x_m = text_start
        la_m = Label(text_x_m, 72, 8*6, 10*8)
        la_m.set_text("m", color=(64, 64, 64), scale=8)

        text_start += 8*6
        text_x_i = text_start
        la_i = Label(text_x_i, 72, 8*6, 10*8)
        la_i.set_text("i",color=(64, 64, 64), scale=8)

        wig_rec = Widget(304, 77, 12, 12)
        wig_rec.set_bg_color((0x70, 0x70, 0x70))

        text_start += 8*4
        text_x_g = text_start
        la_g = Label(text_x_g, 72, 8*6, 10*8)
        la_g.set_text("g",color=(64, 64, 64), scale=8)

        text_start += 8*6
        text_x_o = text_start
        la_o = Label(text_x_o, 72, 8*6, 10*8)
        la_o.set_text("o",color=(64, 64, 64), scale=8)

        ani_A = Animation(la_A2, False) 
        ani_A.set_duration(10)
        ani_A.set_start_value(text_x_A2, 73, 8*6, 10*8)
        ani_A.set_end_value(text_x_A2+30, 76, 8*6, 10*8)
        ani_A.start()

        # #print(value)
        # if app.loading or app.loop > 20:

        #     ui.canvas.draw_string(200 - int(value) * 2, 68 + (int(value) % 8) * 2, "A",
        #                         color=(64, 64, 64), scale=8, mono_space=0)
        #     ui.canvas.draw_string(200 - int(value), 72 + (int(value) % 8), "A",
        #                         color=(0x2d, 0x85, 0xf0), scale=8, mono_space=0)
        # else:
        #     ui.canvas.draw_string(203, 73, "A", color=(
        #         64, 64, 64), scale=8, mono_space=0)

        # if app.loading or app.loop > 40:

        #     ui.canvas.draw_string(203, 72 - int(value) * 5 - 9, "  m",
        #                         color=(64, 64, 64), scale=8, mono_space=0)
        #     ui.canvas.draw_string(200, 70 - int(value) * 4 - 8, "  m",
        #                         color=(0xf4, 0x43, 0x3c), scale=8, mono_space=0)
        # else:
        #     ui.canvas.draw_string(203, 72, "  m",
        #                         color=(64, 64, 64), scale=8, mono_space=0)

        # if app.loading or app.loop > 40:

        #     ui.canvas.draw_string(203, 72, "    i",
        #                         color=(64, 64, 64), scale=8, mono_space=0)
        #     ui.canvas.draw_string(200, 70, "    i",
        #                         color=(0xff, 0xbc, 0x32), scale=8, mono_space=0)

        #     ui.canvas.draw_rectangle((304, 77, 12, 12),
        #                         color=(0x70, 0x70, 0x70), fill=True)

        #     ui.canvas.draw_string(259, 44 + int(value), "    .    ",
        #                         color=(64, 64, 64), scale=4, mono_space=0)
        #     ui.canvas.draw_string(256, 42 + int(value), "    .    ",
        #                         color=(0xff, 0xbc, 0x32), scale=4, mono_space=0)
        # else:
            # ui.canvas.draw_string(203, 72, "    i",
            #                     color=(64, 64, 64), scale=8, mono_space=0)
            # ui.canvas.draw_rectangle((304, 77, 12, 12),
            #                     color=(0x70, 0x70, 0x70), fill=True)
            # ui.canvas.draw_string(259, 44, "    .    ",
            #                     color=(64, 64, 64), scale=4, mono_space=0)

        # if app.loading or app.loop > 60:

        #     ui.canvas.draw_string(203 + int(value) * 2 + 10, 72, "     g",
        #                         color=(64, 64, 64), scale=8, mono_space=0)
        #     ui.canvas.draw_string(200 + int(value) * 2 + 10, 70, "     g",
        #                         color=(0x0a + int(value) * 50, 0xa8, 0x58 + int(value) * 50), scale=8, mono_space=0)
        # else:
        #     ui.canvas.draw_string(203, 72, "     g",
        #                         color=(64, 64, 64), scale=8, mono_space=0)

        # if app.loading or app.loop > 60:

        #     ui.canvas.draw_string(203 - int(value) * 2 + 20, 72, "       o",
        #                         color=(64, 64, 64), scale=8, mono_space=0)
        #     ui.canvas.draw_string(200 - int(value) * 2 + 20, 70, "       o",
        #                         color=(0xf4, 0x43 + int(value) * 50, 0x3c), scale=8, mono_space=0)
        # else:
        #     ui.canvas.draw_string(203, 72, "       o",
        #                         color=(64, 64, 64), scale=8, mono_space=0)

        # if app.loading == False and app.loop < 20:

        #     ui.canvas.draw_string(203, 73, "Amigo",
        #                             color=(64 + int(value) * 2, 64 + int(value) * 2, 64 + int(value) * 2), scale=8, mono_space=0)

        # if app.loop > 70:
        #     app.loading = True;
        #     ui.canvas.draw_string(320, 280, "Now Loading...",
        #                             color=(164 + int(value) * 8, 164 + int(value) * 8, 164 + int(value) * 8), scale=2, mono_space=0)

        # if app.loop == 100:
        #     app.layer += 1

        # ui.display()

if __name__ == '__main__':
    l = LoadPage()

    while True:
        ui.display()
        system.parallel_cycle()