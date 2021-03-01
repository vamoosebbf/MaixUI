import os
import image
try:
    from ui_label import Label
except:
    from ui.ui_label import Label
class Button(Label):
    
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h)

if __name__ == '__main__':
    import time
    try:
        from ui_canvas import ui
        from touch import Touch
        from core import system
    except:
        from ui.ui_canvas import ui
        from driver.touch import Touch
        from lib.core import system

    ui.set_bg_color((0, 255, 0))

    # create button
    btn = Button(0, 0, 80, 80)
    btn.set_text("bbb", scale = 2)
    # btn.set_bg_img(path = os.getcwd() + "/res/icons/app_camera.bmp")
    btn.set_bg_color((255, 0, 255))
    # register event
    def on_press():
        btn.set_bg_color((0,0,255))
        # btn.set_size(100, 100)
        print("btn press")

    def on_release():
        btn.set_bg_color((255, 0, 0))
        # btn.set_size(80, 80)
        print("btn release")
    
    btn.register_event(Touch.press, on_press)
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
    
    ui.add_widget(btn)
    ui.add_widget(btn2)
    ui.add_widget(btn3)
    ui.add_widget(btn4)
    
    ui.remove_widget(btn4)

    clock = time.clock()
    pos_x = 0
    pos_y = 80
    while True:
        clock.tick()
        pos_x +=2
        btn.set_pos_size(pos_x, pos_y, pos_x, pos_y)
        ui.display()
        system.parallel_cycle()
        print(clock.fps())