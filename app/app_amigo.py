# This file is part of MaixUI
# Copyright (c) sipeed.com
#
# Licensed under the MIT license:
#   http://www.opensource.org/licenses/mit-license.php
#

import time, gc, math, image

from pmu_axp173 import AXP173, AXP173_ADDR
from machine import I2C
from fpioa_manager import fm

from Maix import GPIO
from core import agent
from ui_canvas import ui, print_mem_free
from ui_amigo_launcher import launcher
from ui_catch import catch
from ui_pages import pages
from ui_photos import photos
from ui_camera import ai_camera
from fs import OS
from msa301 import MSA301, _MSA301_I2CADDR_DEFAULT
from button import sipeed_button, button_io
from wdt import protect
from led import sipeed_led
from sound import CubeAudio
from touch import Touch, TouchLow
from ui_taskbar import taskbar
from shtxx import SHT3x, SHT3x_ADDR, SHT31_ADDR

#from ui_sample import sample_page
#from ui_explorer import explorer
#from sample_shtxx import sample_shtxx
#from sample_spmod import sample_spmod_test
#from sample_msa301 import sample_msa301

#'''


class app:

    layer = 0  # set help_draw to top
    ctrl = agent()
    btn = sipeed_button()
    loop = 0
    loading = False
    toth = Touch(480, 320, 50)
    touch_select = 0
    msa301 = None
    i2c4 = None

    touch_left = b"\x00\x00\x00\x00\x03\x0F\x3F\xFF\xFF\x3F\x0F\x03\x00\x00\x00\x00\x07\x0F\x3F\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\x3F\x0F\x03"
    touch_right = b"\xE0\xF0\xFC\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFC\xF0\xC0\x00\x00\x00\x00\xC0\xF0\xFC\xFF\xFF\xFC\xF0\xC0\x00\x00\x00\x00"
    touch_close = b"\x00\x1C\x3C\x78\x7C\x6E\x07\x03\x03\x07\x6E\x7C\x78\x3C\x1C\x00\x00\x38\x3C\x1E\x3E\x76\xE0\xC0\xC0\xE0\x76\x3E\x1E\x3C\x38\x00"

    def touch_draw():
        app.toth.event()

        app.loop = (app.loop + 1) % 200

        value = math.cos(math.pi * app.loop / 32) * 8

        # temp code
        tmp_x, tmp_l, tmp_r = 0, 0, 0

        if app.toth.state == 2:
          print(app.toth.state, app.toth.points)
          p = app.toth.points[1]
          if p[0] > 430 and p[1] > 260:
            app.layer -= 1
            app.exit_application()
          elif p[0] < 60 and p[1] < 60:
            app.touch_select = -1
            #print(app.touch_select)
            if launcher.app_select == 1:
                app.current.page -= 1
            elif launcher.app_select == 3:
                photos.image_last()
            elif launcher.app_select == 0:
                ai_camera.back()
          elif p[0] > 420 and p[1] < 60:
            app.touch_select = +1
            #print(app.touch_select)
            if launcher.app_select == 1:
                app.current.page -= 1
            elif launcher.app_select == 3:
                photos.image_last()
            elif launcher.app_select == 0:
                ai_camera.next()

        if app.toth.state == 1:
            p = app.toth.points[1]
            if p[0] > 430 and p[1] > 270:
                tmp_x = int(value) + 30
            elif p[0] < 50 and p[1] < 50:
                tmp_l = int(value) + 30
            elif p[0] > 430 and p[1] < 50:
                tmp_r = int(value) + 30

        ui.canvas.draw_circle(ui.height, 0, 40 + tmp_x,
                              thickness=8, fill=False, color=(100, 100, 100))
        ui.canvas.draw_circle(ui.height, 0, 38 + tmp_x,
                              fill=True, color=(255, 255, 255))
        #ui.canvas.draw_string(ui.height - 15, 5, "x", scale=2, color=(0, 0, 0))
        ui.canvas.draw_font(ui.height - 22, 8, 16, 16,
                            app.touch_close, scale=1, color=(155, 155, 0))

        ui.canvas.draw_circle(0, ui.weight, 40 + tmp_l,
                              thickness=8, fill=False, color=(100, 100, 100))
        ui.canvas.draw_circle(0, ui.weight, 38 + tmp_l,
                              fill=True, color=(255, 255, 100))
        #ui.canvas.draw_string(10, ui.weight - 30, "<", scale=2, color=(0, 0, 0))
        ui.canvas.draw_font(8, ui.weight - 25, 16, 16,
                            app.touch_left, scale=1, color=(155, 155, 0))

        ui.canvas.draw_circle(ui.height, ui.weight, 40 + tmp_r,
                              thickness=8, fill=False, color=(100, 100, 100))
        ui.canvas.draw_circle(ui.height, ui.weight, 38 +
                              tmp_r, fill=True, color=(100, 255, 255))
        #ui.canvas.draw_string(ui.height - 15, ui.weight - 30, ">", scale=2, color=(0, 0, 0))
        ui.canvas.draw_font(ui.height - 20, ui.weight - 25, 16,
                            16, app.touch_right, scale=1, color=(0, 155, 155))

    #@ui.warp_template(CubeAudio.event)
    @ui.warp_template(ui.bg_in_draw)
    #@ui.warp_template(ui.help_in_draw)
    def draw_load():

        app.loop = (app.loop + 1) % 200

        value = math.cos(math.pi * app.loop / 8) * 6

        #print(value)
        if app.loading or app.loop > 20:

            ui.canvas.draw_string(200 - int(value) * 2, 68 + (int(value) % 8) * 2, "A",
                                color=(64, 64, 64), scale=8, mono_space=0)
            ui.canvas.draw_string(200 - int(value), 72 + (int(value) % 8), "A",
                                color=(0x2d, 0x85, 0xf0), scale=8, mono_space=0)
        else:
            ui.canvas.draw_string(203, 73, "A", color=(
                64, 64, 64), scale=8, mono_space=0)

        if app.loading or app.loop > 40:

            ui.canvas.draw_string(203, 72 - int(value) * 5 - 9, "  m",
                                color=(64, 64, 64), scale=8, mono_space=0)
            ui.canvas.draw_string(200, 70 - int(value) * 4 - 8, "  m",
                                color=(0xf4, 0x43, 0x3c), scale=8, mono_space=0)
        else:
            ui.canvas.draw_string(203, 72, "  m",
                                color=(64, 64, 64), scale=8, mono_space=0)

        if app.loading or app.loop > 40:

            ui.canvas.draw_string(203, 72, "    i",
                                color=(64, 64, 64), scale=8, mono_space=0)
            ui.canvas.draw_string(200, 70, "    i",
                                color=(0xff, 0xbc, 0x32), scale=8, mono_space=0)

            ui.canvas.draw_rectangle((304, 77, 12, 12),
                                color=(0x70, 0x70, 0x70), fill=True)

            ui.canvas.draw_string(259, 44 + int(value), "    .    ",
                                color=(64, 64, 64), scale=4, mono_space=0)
            ui.canvas.draw_string(256, 42 + int(value), "    .    ",
                                color=(0xff, 0xbc, 0x32), scale=4, mono_space=0)
        else:
            ui.canvas.draw_string(203, 72, "    i",
                                color=(64, 64, 64), scale=8, mono_space=0)
            ui.canvas.draw_rectangle((304, 77, 12, 12),
                                color=(0x70, 0x70, 0x70), fill=True)
            ui.canvas.draw_string(259, 44, "    .    ",
                                color=(64, 64, 64), scale=4, mono_space=0)

        if app.loading or app.loop > 60:

            ui.canvas.draw_string(203 + int(value) * 2 + 10, 72, "     g",
                                color=(64, 64, 64), scale=8, mono_space=0)
            ui.canvas.draw_string(200 + int(value) * 2 + 10, 70, "     g",
                                color=(0x0a + int(value) * 50, 0xa8, 0x58 + int(value) * 50), scale=8, mono_space=0)
        else:
            ui.canvas.draw_string(203, 72, "     g",
                                color=(64, 64, 64), scale=8, mono_space=0)

        if app.loading or app.loop > 60:

            ui.canvas.draw_string(203 - int(value) * 2 + 20, 72, "       o",
                                color=(64, 64, 64), scale=8, mono_space=0)
            ui.canvas.draw_string(200 - int(value) * 2 + 20, 70, "       o",
                                color=(0xf4, 0x43 + int(value) * 50, 0x3c), scale=8, mono_space=0)
        else:
            ui.canvas.draw_string(203, 72, "       o",
                                color=(64, 64, 64), scale=8, mono_space=0)

        if app.loading == False and app.loop < 20:

            ui.canvas.draw_string(203, 73, "Amigo",
                                  color=(64 + int(value) * 2, 64 + int(value) * 2, 64 + int(value) * 2), scale=8, mono_space=0)

        if app.loop > 70:
            app.loading = True;
            ui.canvas.draw_string(320, 280, "Now Loading...",
                                  color=(164 + int(value) * 8, 164 + int(value) * 8, 164 + int(value) * 8), scale=2, mono_space=0)

        if app.loop == 100:
            app.layer += 1

        ui.display()

    # @ui.warp_template(ui.bg_in_draw) # ui_3d_launcher need remove
    @ui.warp_template(launcher.draw)
    #@ui.warp_template(taskbar.mem_draw)
    @ui.warp_template(taskbar.battery_draw)
    @ui.warp_template(ui.bg_in_draw)
    def draw_launcher():
        ui.display()

    #@ui.warp_template(CubeAudio.event)
    @ui.warp_template(ui.grey_draw)
    @ui.warp_template(ui.anime_draw)
    @ui.warp_template(touch_draw)
    #@ui.warp_template(CubeAudio.event)
    #@ui.warp_template(taskbar.mem_draw)
    # @ui.warp_template(system_info.info_draw)
    def draw_pages():
        if app.current != None:
            app.current.draw()

        app.loop = (app.loop + 1) % 200

        value = math.cos(math.pi * app.loop / 12) * 2 + 20
        for i in range(100):
            try:
                #ui.canvas.draw_rectangle((240, 0, 240, 320), fill=False, thickness=3, color=(175, 175, 175))
                if app.msa301 != None:
                    accel = app.msa301.acceleration
                    x, y = 240, 160 # center
                    #print(accel)
                    ui.canvas.draw_circle(x + int(accel[0] * 15), y + int(accel[1] * 20), int(value), fill=True,
                        color=(150 + int(accel[0] * 20), 150 + int(accel[1] * 20), 100 + int(accel[2] * 20)))  # 10ms
                    ui.canvas.draw_circle(x + int(accel[0] * 15), y + int(accel[1] * 20), int(value) + 1, thickness=3, fill=False, color=(0, 0, 0))  # 10ms
                else:

                    app.msa301 = MSA301(app.i2c3)
                break
            except Exception as e:
                pass
                # gc.collect()
        #ui.canvas.draw_string(240 + 10, 140, "x", (255, 0, 0), scale=2)
        #ui.canvas.draw_string(240 + 10, 140, "x", (255, 0, 0), scale=2)
        #ui.canvas.draw_line(240 + 120, 150, 120 + int(accel[0] * 8), 150, color=(41, 131, 255))
        #ui.canvas.draw_string(240 + 10, 160, "y", (0, 255, 0), scale=2)
        #ui.canvas.draw_line(240 + 120, 170, 120 + int(accel[1] * 8), 170, color=(141, 31, 255))
        #ui.canvas.draw_string(240 + 10, 180, "z", (0, 0, 255), scale=2)
        #ui.canvas.draw_line(240 + 120, 190, 120 + int(accel[2] * 8), 190, color=(241, 131, 55))

        ui.display()

    photos_title = "/"
    photos_temp = None
    #@ui.warp_template(taskbar.time_draw)
    #@ui.warp_template(sample_page.sample_draw)
    #@ui.warp_template(ui.grey_draw)
    #@ui.warp_template(CubeAudio.event)
    #@ui.warp_template(touch_draw)
    def draw_photos():
        if photos.photos_len() > 0:

            if app.photos_title != photos.image_path():
                app.photos_title = photos.image_path()
                if app.photos_temp != None:
                    tmp = app.photos_temp
                    del tmp
                    app.photos_temp = None
            if app.photos_temp:
                ui.canvas.draw_image(app.photos_temp, 0, 0)
            else:
                app.photos_temp = image.Image(app.photos_title)


            # [mem < 800*1024]
            #t, ui.canvas = ui.canvas, None
            #del t
            #ui.canvas = image.Image(photos.image_path())

            ui.canvas.draw_string(2, 2, app.photos_title, color=(255, 255, 255), scale=1, mono_space=0)
        else:
            ui.canvas.draw_string(40, 120, "Please put pictures\n in '/sd/imgs' folder", color=(255, 255, 255), scale=3, mono_space=0)
        app.touch_draw()
        ui.display()

    sht3x = None
    sidu = None
    temp = 0
    points = []
    isconnected = False
    @ui.warp_template(touch_draw)
    #@ui.warp_template(taskbar.mem_draw)
    #@ui.warp_template(taskbar.time_draw)
    @ui.warp_template(CubeAudio.event)
    #@ui.warp_template(explorer.draw)
    def draw_demo():
        app.loop = (app.loop + 1) % 200
        value = math.cos(math.pi * app.loop / 16) * 10

        ui.canvas.draw_string(10, 5, "Seeed Grove",
                          color=(40 + int(value) * 2, 240 + int(value) * 2, 40 + int(value) * 2), scale=3, mono_space=0)

        try:
            CubeAudio.event()
            if app.isconnected == False:
                CubeAudio.event()

                if app.loop % 5 == 1:
                    result = app.i2c4.scan()
                    ui.canvas.draw_string(290, 80, "Scan Dev: " + str(result),
                                          color=(140 + int(value) * 5, 240 + int(value) * 5, 140 + int(value) * 5), scale=2, mono_space=0)

                    if SHT3x_ADDR in result:
                        app.sht3x = SHT3x(app.i2c4, SHT3x_ADDR)
                        app.isconnected = True
                    CubeAudio.event()
                    if SHT31_ADDR in result:
                        app.sht3x = SHT3x(app.i2c4, SHT31_ADDR)
                        app.isconnected = True
                    CubeAudio.event()

                ui.canvas.draw_string(280, 25, "Wait Grove Sensor \n sht31/35 <<<  <<  <-",
                                      color=(140 + int(value) * 5, 240 + int(value) * 5, 140 + int(value) * 5), scale=2, mono_space=0)

                if CubeAudio.event() == False:

                    value = math.cos(math.pi * app.loop / 100) * 50

                    tmp = int(value)
                    #print(value)

                    ui.canvas.draw_circle(0, 0, 100 + tmp, fill=False, color=(0, (150 + tmp) + 10, 0))
                    ui.canvas.draw_circle(0, 0, 100 + tmp * 2, fill=False, color=(0, (150 + tmp) + 20, 0))
                    ui.canvas.draw_circle(0, 0, 100 + tmp * 3, fill=False, color=(0, (150 + tmp) + 30, 0))
                    ui.canvas.draw_circle(0, 0, 100 + tmp * 4, fill=False, color=(0, (150 + tmp) + 40, 0))

            else:
                data = app.sht3x.read_temp_humd()
                # print(data)
                if app.sidu == None:
                    app.sidu = image.Image(os.getcwd() + "/res/images/sidu.jpg")

                ui.canvas.draw_circle(350, 160, 100, fill=True, color=(255, 255, 255))
                ui.canvas.draw_image(app.sidu, 270, 60, alpha=235 + int(value) * 2)
                ui.canvas.draw_string(330, 190, "%.2d" % data[1], scale=4, color=(80, 80, 80))

                ui.canvas.draw_rectangle(60, 60, 180, 200, thickness=4, color=(155, 155, 155))
                if len(app.points) > 18:
                    app.points.pop(0)
                elif data[0] > 1 and app.temp != int(data[0] * 10):
                    app.temp = int(data[0] * 10)
                    app.points.append(app.temp)
                for p in range(len(app.points)):
                    #print(app.points)
                    if p < 1:
                        b = (60 + int(10 * (p))), 450 - app.points[p]
                        ui.canvas.draw_circle(b[0], b[1], 3, fill=True, color=(255, 155, 150))
                    else:
                        a, b = ((60 + int(10 * (p-1))), 450 - app.points[p-1]), ((60 + int(10 * (p))), 450 - app.points[p])
                        ui.canvas.draw_circle(b[0], b[1], 3, fill=False, color=(155, 155, 155))
                        ui.canvas.draw_line(a[0], a[1], b[0], b[1], thickness=4, color=(255,255,255))

                ui.canvas.draw_string(60, 280, "Average temperature: %s" % str(sum(app.points) / len(app.points) / 10.0),
                                      color=(240 + int(value) * 5, 240 + int(value) * 5, 240 + int(value) * 5), scale=2, mono_space=0)

            CubeAudio.event()
            ui.display()
        except Exception as e:
            app.layer = 1
            app.isconnected = False
            app.points=[]
            raise e

    def draw_camera():
        try:
            gc.collect()
            ai_camera.ai_draw()
            for model in ai_camera.models:
              #print(model.__qualname__, ai_camera.model.__qualname__)
              if 'ai_sample' == ai_camera.model.__qualname__:
                  ui.canvas.draw_string(340, 80, "  AI\nDemo", scale=5)
                  ui.canvas.draw_string(50, 260, "Press Left (<) or Right (>) to View", scale=2)
                  pass

              elif 'FaceDetect' == ai_camera.model.__qualname__:

                    if ai_camera.model.bbox != None:
                        bbox = ai_camera.model.bbox
                        ui.canvas.draw_string(50, 260, "Face Detect %d" % len(bbox), scale=5)
                        for pos in range(len(bbox)):
                            i = bbox[pos]
                            # print(i.x(), i.y(), i.w(), i.h())
                            face_cut = ui.canvas.cut(i.x(), i.y(), i.w(), i.h())
                            face_cut_128 = face_cut.resize(80, 80)
                            ui.canvas.draw_image(face_cut_128, 320 + int((pos % 2)*80), int((pos // 2)*80))
                    else:
                        ui.canvas.draw_string(50, 260, "Find Detect", scale=5)

              elif 'FaceReco' == ai_camera.model.__qualname__:
                    ui.canvas.draw_string(50, 260, "Face Recognition", scale=5)

              elif 'find_color' == ai_camera.model.__qualname__:

                    ui.canvas.draw_string(50, 260, "Find Color For Red (53, 31, 44, 82, 18, 78)", scale=2)
                    ui.canvas.draw_string(50, 260, "                         Red", color=(255,0,0), scale=2)

                    ui.canvas.draw_string(340, 30, "Red\nSum\n  %d" % len(ai_camera.model.blobs), scale=5)

              elif 'HowMany' == ai_camera.model.__qualname__:

                    if ai_camera.model.things != None:
                        ui.canvas.draw_string(340, 30, "How\nMany\n  %d" % len(ai_camera.model.things), scale=5)

                    ui.canvas.draw_string(50, 260, "How many things are there?", scale=2)

              elif 'MaybeIs' == ai_camera.model.__qualname__:

                    ui.canvas.draw_string(340, 50, "Maybe\n   Is\n", scale=3)
                    ui.canvas.draw_string(340, 150, "%s" % str(ai_camera.model.result), scale=2)
                    ui.canvas.draw_string(50, 260, "What is likely to be?", scale=2)

              elif 'MoblieNet' == ai_camera.model.__qualname__:

                    ui.canvas.draw_string(340, 50, "MoblieNet\n   1000class\n", scale=3)
                    ui.canvas.draw_string(340, 150, "What is likely to be?", scale=2)

            app.touch_draw()
            ui.display()
        except Exception as e:
            # ai_camera.next()
            # protect.restart() # temp patch
            app.layer -= 1
            raise e
            #raise Exception("This is a Easter egg(Known Bug) This error requires a  restart. It will soon be resolved. :)")

    current = None

    def load_application(selected):
        if app.current != None: # clear last application
            del app.current
            app.current = None
        if selected == 0:
            pass

        elif selected == 1:
            app.current = pages()
            app.current.tips = "Weclome to Maix Amigo"
        elif selected == 2:
            CubeAudio.load(os.getcwd() + "/res/sound/loop.wav", 100)
            app.points=[]
            pass
            #app.layer -= 1 # return last layer
            #raise Exception("Settings Unrealized.")
        elif selected == 3:
            photos.scan()

    def exec_application():
        try:
            if launcher.app_select == 0:
                app.draw_camera()
            if launcher.app_select == 1:
                app.draw_pages()
            if launcher.app_select == 2:
                app.draw_demo()
            if launcher.app_select == 3:
                app.draw_photos()
        except Exception as e:
            app.layer -= 1
            raise e

    def exit_application():
        try:
            if launcher.app_select == 0:
                ai_camera.exit()
                ai_camera.jump(0)
                ai_camera.reload()
            elif launcher.app_select == 1:
                pass
            elif launcher.app_select == 2:
                t, app.sidu = app.sidu, None # Clear
                del t
            elif launcher.app_select == 3:
                t, app.photos_temp = app.photos_temp, None # Clear
                del t
        except Exception as e:
            app.layer -= 1
            raise e

    rgb = 0
    def rgb_change(rgb):
        sipeed_led.r.value(rgb & 0b001)
        sipeed_led.g.value(rgb & 0b010)
        sipeed_led.b.value(rgb & 0b100)

    def on_event():
        #app.btn.event()
        app.btn.expand_event()
        if app.btn.home() == 2 or launcher.app_run: # click button release to 2
            launcher.app_run = False
            print('into', app.layer)
            if app.layer == 1:
                app.layer += 1
                # launcher into application
                app.load_application(launcher.app_select)
            elif app.layer == 2:
                if app.btn.interval() > 1000: # long press
                    app.layer -= 1
                    app.exit_application()
                # application return launcher
            else:
                app.layer += 1
                # help into launcher
        #launcher.btn.enable = True

        #if launcher.app_run:
            #launcher.app_run = False
            #print('launcher.app_select', launcher.app_select)

        if app.btn.next() == 1:
            app.rgb = (app.rgb + 1) % 8
            app.rgb_change(app.rgb)
            if launcher.app_select == 3:
                photos.image_next()

        if app.btn.back() == 1:
            app.rgb = (app.rgb - 1) % 8
            app.rgb_change(app.rgb)
            if launcher.app_select == 3:
                photos.image_last()

    @ui.warp_template(ui.blank_draw)
    #@ui.warp_template(ui.grey_draw)
    @catch
    def draw():
        app.on_event()
        ui.canvas.draw_rectangle((0, 0, ui.height, ui.weight),
                                      fill = True, color = (0x70, 0x70, 0x70))

        # gc.collect()
        if app.layer == 0:
            app.draw_load()
        elif app.layer == 1:
            app.draw_launcher()
        elif app.layer == 2:
            app.exec_application()

    def run():
        # debug into app_select
        # launcher.app_select = 2
        # app.layer = 1

        ui.height, ui.weight = 480, 320
        # button_io.config(23, 20, 31) # amigo tft
        button_io.config(16, 23, 20) # amigo ips
        sipeed_led.init(14, 15, 17, 32)


        app.i2c3 = I2C(I2C.I2C3, freq=100*1000, scl=24, sda=27)
        app.i2c4 = I2C(I2C.I2C4, freq=100*1000, scl=9, sda=7)

        TouchLow.config(i2c3=app.i2c3) # amigo

        #if AXP173_ADDR in i2c.scan():
        axp173 = AXP173(i2c_dev=app.i2c3)
        axp173.enable_adc(True)
        # 默认充电限制在 4.2V, 190mA 档位
        axp173.setEnterChargingControl(True)
        axp173.exten_output_enable()
        # amigo sensor config.
        axp173.writeREG(0x27, 0x20)
        axp173.writeREG(0x28, 0x0C)
        taskbar.init(axp173)

        CubeAudio.init(app.i2c3)
        if CubeAudio.check():
            CubeAudio.ready()
            fm.register(13,fm.fpioa.I2S0_MCLK, force=True)
            fm.register(21,fm.fpioa.I2S0_SCLK, force=True)
            fm.register(18,fm.fpioa.I2S0_WS, force=True)
            fm.register(35,fm.fpioa.I2S0_IN_D0, force=True)
            fm.register(34,fm.fpioa.I2S0_OUT_D2, force=True)

        #app.ctrl.event(100, lambda *args: time.sleep(1))
        #app.ctrl.event(10, app.on_event)
        app.ctrl.event(5, app.draw)
        #ui.enable = False
        while True:
            last = 0
            while True:
                try:
                    # print((int)(1000 / (time.ticks_ms() - last)), 'fps')
                    # last = time.ticks_ms()
                    # print_mem_free()
                    gc.collect()
                    app.ctrl.cycle()
                    protect.keep()
                    #time.sleep(0.1)
                except KeyboardInterrupt:
                    protect.stop()
                    raise KeyboardInterrupt()
                except Exception as e:
                    # gc.collect()
                    print(e)

#'''
if __name__ == "__main__":
    import lcd
    from Maix import utils
    import machine

    if utils.gc_heap_size() != 1024*1024:
        utils.gc_heap_size(1024*1024) # 1MiB
        machine.reset()
    
    lcd.init()
    print_mem_free()
    app.run()
