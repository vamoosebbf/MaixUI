# This file is part of MaixUI
# Copyright (c) sipeed.com
#
# Licensed under the MIT license:
#   http://www.opensource.org/licenses/mit-license.php
#

import time
from fpioa_manager import fm
from Maix import GPIO
from machine import I2C

try:
    from core import system
except ImportError:
    from lib.core import system

FT_DEVIDE_MODE = 0x00
FT_ID_G_MODE = 0xA4
FT_ID_G_THGROUP = 0x80
FT_ID_G_PERIODACTIVE = 0x88

FT6X36_ADDR = 0x38

class TouchLow:
  i2c3 = None
  addr = 0x0

  def config(i2c, addr=FT6X36_ADDR):
    TouchLow.i2c = i2c
    TouchLow.addr = addr

  def write_reg(reg_addr, buf):
    TouchLow.i2c.writeto_mem(TouchLow.addr, reg_addr, buf, mem_size=8)

  def read_reg(reg_addr, buf_len):
    return TouchLow.i2c.readfrom_mem(TouchLow.addr, reg_addr, buf_len, mem_size=8)

  def config_ft6x36():
    TouchLow.write_reg(FT_DEVIDE_MODE, 0); # 进入正常操作模式
    TouchLow.write_reg(FT_ID_G_THGROUP, 12); # 设置触摸有效值，触摸有效值，12，越小越灵敏
    TouchLow.write_reg(FT_ID_G_PERIODACTIVE, 14); # 激活周期，不能小于12，最大14

  def get_point():
    if TouchLow.i2c != None:
      #data = self.read_reg(0x01, 1)
      #print("get_gesture:" + str(data))
      data = TouchLow.read_reg(0x02, 1)
      #print("get_points:" + str(data))
      if (data != None and data[0] == 0x1):
          data_buf = TouchLow.read_reg(0x03, 4)
          y = ((data_buf[0] & 0x0f) << 8) | (data_buf[1])
          x = ((data_buf[2] & 0x0f) << 8) | (data_buf[3])
          #print("1 point[{}:{}]".format(x,y))
          if ((data_buf[0] & 0xc0) == 0x80):
              #print("2 point[({},{}):({},{})]".format(
                  #x, y,  self.width - x, self.height - y))
              return (x, y)
    return None

class Touch:

  click, idle, press, release = "Touch.click", "Touch.idle", "Touch.press", "Touch.release"
  
  def __init__(self, i2c, w, h, cycle=1000, irq_pin = 33):
    self.cycle = cycle
    self.last_time = 0
    self.points = [(0, 0, 0), (0, 0, 0)]
    self.state = Touch.idle
    self.width, self.height = w, h
    
    # touch dirver init
    if i2c == None:
      i2c = I2C(I2C.I2C3, freq=100*1000, scl=24, sda=27) # amigo
    TouchLow.config(i2c=i2c) 
    
    # 触摸事件
    self.events = []
    fm.register(irq_pin, fm.fpioa.GPIOHS2, force=True)
    key=GPIO(GPIO.GPIOHS2,GPIO.IN, GPIO.PULL_DOWN)
    key.irq(self.press_check, GPIO.IRQ_FALLING, GPIO.WAKEUP_NOT_SUPPORT, 7)

    system.event(5, self.release_check)

  # 松手检测, 轮询检测
  def release_check(self):        
    # timeout return ilde.
    if (time.ticks_ms() > self.last_time + self.cycle) and (self.state != Touch.idle):
        if self.state == Touch.click:
            self.state = Touch.idle
            self.points = [(0, 0, 0), (0, 0, 0)]
        if self.state == Touch.press:
            self.state = Touch.click
        self._events_cycle() # 通知所有已注册 touch event 控件

  # 按压检测, 中断触发
  def press_check(self, num):
    tmp = TouchLow.get_point()
    if tmp != None:
      x, y = tmp
      y = self.height - y
      self.last_time = time.ticks_ms()
      if self.state != Touch.press:
          self.state = Touch.press
          self.points[0] = (x, y, time.ticks_ms())
      self.points[1] = (x, y, time.ticks_ms())
      self._events_cycle() # 通知所有已注册 touch event 控件

  def _events_cycle(self):
    for eve in self.events:
        eve[0](eve[1:]) if eve[1:] else eve[0]()
  
  def register_touch_event(self, func, *args):
    self.events.append([func, args])

  def unregister_touch_event(self, func, *args):
    for i in self.events:
      if i == [func, args]:
            self.events.remove(i)

touch = Touch(i2c = None, w = 480, h = 320, cycle = 50, irq_pin = 33)

if __name__ == '__main__':
    def on_touch(s):
        print(touch.state)
    s = "touch it"
    a = 1
    touch.register_touch_event(on_touch, s, a)
    while  True:
        system.parallel_cycle()
    