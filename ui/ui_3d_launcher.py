# This file is part of MaixUI
# Copyright (c) sipeed.com
#
# Licensed under the MIT license:
#   http://www.opensource.org/licenses/mit-license.php
#

import math, os, image, gc

try:
    from ui_canvas import ui
    from button import sipeed_button
    from core import agent
except ImportError:
    from ui.ui_canvas import ui
    from driver.button import sipeed_button
    from lib.core import agent

class icon:

  x, y, w, h, img = 0, 0, 0, 0, None

  def __init__(self, x, y, path):
    self.x, self.y = x, y
    self.img = image.Image(path)

  def checked(self, img, color=(255, 0, 0), x = None, y = None):
    ui.canvas.draw_rectangle(x - 2, y - 2,
                             img.width + 4, img.height + 4, color, thickness=1)

  def draw(self, is_check=False, alpha=0, color=(255, 255, 255), x = None, y = None, scale = 1.0):
    img = self.img
    if x == None:
        x = self.x
    if y == None:
        y = self.y
    if is_check:
      self.checked(img, color, x=x, y=y)
    try:
      tmp = img.resize(int(img.width() * scale), int(img.height() * scale))
      ui.canvas.draw_image(tmp, x, y, alpha=int(alpha))  # 4ms
      del tmp
    except MemoryError as e:
      print('resize uncertain', (int(img.width() * scale), int(img.height() * scale)))
      try:
        ui.canvas.draw_image(img, x, y, alpha=int(alpha))  # 4ms
      except MemoryError as e:
        print('resize fail')
        pass

  def title(self, string, color=(255, 255, 255)):
    ui.canvas.draw_string(self.x, self.y, string)


class launcher:

  alpha = 0
  app_select = 0
  app_sets = [
      icon(40, 50, os.getcwd() + "/res/icons/app_camera.bmp"),
      icon(140, 50, os.getcwd() + "/res/icons/app_settings.bmp"),
      icon(40, 150, os.getcwd() + "/res/icons/app_explorer.bmp"),
      icon(140, 150, os.getcwd() + "/res/icons/app_system_info.bmp")
  ]

  btn = sipeed_button()
  agent = agent()

  def init():
    launcher.agent.event(100, launcher.key_event)

  def key_event():
    launcher.btn.event()

    if launcher.btn.back() == 1:
        if launcher.goal == 0:
            launcher.goal = -30
    elif launcher.btn.next() == 1:
        if launcher.goal == 0:
            launcher.goal = +30
    # elif launcher.btn.home() == 2:
    #     print('start', launcher.app_select)

        # ui.canvas.draw_string(15, 120, '(%s)' % launcher.app_sets[launcher.app_select])

    #launcher.goal = launcher.goal % 120 # lock pos

  pos, goal = 0, 0

  def load(app_pos, app_select):
    pos = app_pos * (math.pi / 60)
    tmp = (120 * math.sin(pos), 30 * math.cos(pos + 0.35))

    #ui.canvas.draw_line(120, 100, 120 + int(tmp[0]), 120 + int(tmp[1]), color=(150, 150, 150))
    #ui.canvas.draw_circle((100, 60, 5), color=(255, 136, 210))
    #ui.canvas.draw_line(100, 60, 100, 100, color=(255, 136, 210))

    x, y = (120 + int(tmp[0] - 30)), (120 + int(tmp[1] - 30))
    s = (y / 120) * 1.5
    #if int(y * s - y - 60) > 0:
    alpha=int((y / 100) ** 4 * 100 + 40)
    # print('alpha', alpha)
    launcher.app_sets[app_select].draw(is_check=False, alpha=alpha, x=x-15, y=int(y * s - y), scale=s)

  def draw():
    launcher.agent.parallel_cycle()
    launcher.app_select = int(launcher.pos / 30)

    if launcher.goal == 0:
        pass
    elif launcher.goal > 0:
        launcher.goal -= 5
        launcher.pos += 5
    elif launcher.goal < 0:
        launcher.goal += 5
        launcher.pos -= 5

    launcher.pos = launcher.pos % 120 # lock pos

    value = (launcher.pos % 30)

    color = (100 + 5 *value, 100 + 5 *value, 100 + 5 * value)
    #print(color)
    ui.canvas.draw_ellipse(130, 150, 90 + (value % 20 - 10), 40 + (value % 20 - 10), -10, color=color, thickness=2 + value % 5, fill=False)
    # gc.collect()
    launcher.load(launcher.pos, 0)
    launcher.load(launcher.pos - 30, 1)
    launcher.load(launcher.pos - 60, 2)
    launcher.load(launcher.pos - 90, 3)
    #launcher.load(launcher.pos - 80, 0)
    #launcher.load(launcher.pos - 100, 1)

    #value = math.cos(math.pi * launcher.alpha / 12) * 50 + 200
    #launcher.alpha = (launcher.alpha + 1) % 24

    #for pos in range(0, 4):
        #checked = (pos == launcher.app_select)
        #launcher.app_sets[pos].draw(checked, value if checked else 255)

launcher.init()

if __name__ == "__main__":
  from ui_canvas import ui
  from ui_taskbar import taskbar

  @ui.warp_template(ui.blank_draw)
  @ui.warp_template(ui.grey_draw)
  # @ui.warp_template(ui.bg_in_draw)
  @ui.warp_template(launcher.draw)
  @ui.warp_template(taskbar.time_draw)
  def unit_test():
    ui.display()
  import time
  last = time.ticks_ms()
  while True:
      print(time.ticks_ms() - last)
      last = time.ticks_ms()
      unit_test()
      #time.sleep(0.01)
