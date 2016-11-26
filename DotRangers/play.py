from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice
from subprocess import call

class Utility:
    def __init__(self):
        self.load = {}
        call(["adb", "devices"])
        print 'waitting for connection'
        self.device = MonkeyRunner.waitForConnection()

    def back(self, delay = 1):
        print 'back, wait %ds' %(delay)
        self.device.press('KEYCODE_BACK', MonkeyDevice.DOWN_AND_UP)
        MonkeyRunner.sleep(delay)

    def check(self, name, pos, match, img = False):
        print 'check ' + name

        if img == False:
            print 'take snapshot'
            img = self.device.takeSnapshot()

        self.load[name] = MonkeyRunner.loadImageFromFile('./' + name + '.png','png') 
        sub = img.getSubImage(pos)
        sub.writeToFile('./1.png')
        return sub.sameAs(self.load[name], match)

    def click(self, name, delay = 1):
        pos = self.positions[name]
        x = pos['x']
        y = pos['y']

        print 'click, %s (%d,%d), wait %ds' %(name, x, y, delay)
        self.device.touch(x, y, MonkeyDevice.DOWN_AND_UP)
        MonkeyRunner.sleep(delay)

    def drag(self, **kwargs):
        print kwargs.msg
        self.device.drag(kwargs.start, kwargs.end, kwargs.duration, kwargs.steps)
        MonkeyRunner.sleep(kwargs.delay)

    def hold(self, **args):
        name = args['name']
        pos = self.positions[name]
        x = pos['x']
        y = pos['y']
        duration = args.get('duration', 1)
        steps = args.get('steps', 10)
        delay = args.get('delay', 1)

        print 'hold %s (%d, %d), %fs (%d), wait %ds' %(name, x, y, duration, steps, delay)
        self.device.drag((x,y), (x,y), duration, steps)
        MonkeyRunner.sleep(delay)

    def pixel(self, *args):
        if len(args) == 1:
            name1 = args[0]
            name2 = args[0]
            img = False
        elif len(args) == 2:
            if isinstance(args[1], basestring):
                name1 = args[0]
                name2 = args[1]
                img = False
            else:
                name1 = args[0]
                name2 = args[0]
                img = args[1]
        else:
            name1 = args[0]
            name2 = args[1]
            img = args[2]

        pos = self.positions[name1]
        color = self.colors[name2]
        x = pos['x']
        y = pos['y']
        print 'pixel %s (%d, %d), %s ' %(name1, x, y, name2),

        if img == False:
            img = self.device.takeSnapshot()

        p = img.getRawPixel(x, y)
        print p
        return p == color

class DotRangers:
    def __init__(self):
        self.util = Utility()
        self.device = self.util.device

        self.util.positions = {
            'ad': { 'x': 687, 'y': 685 },
            'ad yes': { 'x': 500, 'y': 530 },
        }
        self.util.colors = {
            'ad': (-1,33,33,33),
        }

    def watch(self):
        while (not self.util.pixel('ad')):
            print 'no'

self = DotRangers()
while True:
    self.watch()
    self.util.click('ad')
    self.util.click('ad yes')
    self.util.back()
