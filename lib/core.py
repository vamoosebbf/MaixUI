
# This file is part of MaixUI
# Copyright (c) sipeed.com
#
# Licensed under the MIT license:
#   http://www.opensource.org/licenses/mit-license.php
#

class agent:

    def __init__(self):
        self.msg = []  # [][4] 类型， [][0] 时间, [][1] 周期， [][2] 函数， [][3] 参数

    def get_ms(self):
        import time
        return time.ticks_ms()

    # add envent
    def event(self, cycle, func, args=None):
        # arrived, cycle, function
        tmp = (self.get_ms() + cycle, cycle, func, args)
        self.msg.append(tmp)

    def remove(self, func):
        for pos in range(len(self.msg)):  # maybe use map
            if self.msg[pos][2] == func:
                print("remove", func)
                self.msg.remove(self.msg[pos])
                break

    def call(self, obj, pos=0):
        try:
            self.msg.pop(pos)
        except:
            return
        self.event(obj[1], obj[2], obj[3])
        obj[2](obj[3]) if obj[3] else obj[2]()  # exec function

    # 执行第一个 event
    def cycle(self):
        if (len(self.msg)):
            obj = self.msg[0]
            if (self.get_ms() >= obj[0]):
                self.call(obj, 0)

    # 顺序执行所有 event
    def parallel_cycle(self):
        funcs = []
        for pos in range(len(self.msg)):  # maybe use map
            obj = self.msg[pos]
            if (self.get_ms() >= obj[0]):
                self.call(obj, pos)
                break
        #         funcs.append([obj, pos])
        # for func in funcs:
        #     self.call(func[0], func[1])


system = agent()

if __name__ == "__main__":
    class tmp:
        def __init__(self):
            print('init', __class__.test_1)

            setattr(self, "test0", self.test_0)
            setattr(self, "test1", self.test_1)
            system.event(200, self.test0)
            system.event(10, self.test1)
            system.event(2000, self.test_2)

        def test_0(self):
            print('test_0')

        def test_1(self):
            print('test_1')

        def test_2(self):
            print('test_2', self.test_1)
            system.remove(self.test1)
            # system.remove(self.test_2)

        def unit_test(self):
            import time
            clock = time.clock()
            while True:
                clock.tick()
                system.parallel_cycle()
                print(clock.fps())
    a = tmp()
    a.unit_test()
