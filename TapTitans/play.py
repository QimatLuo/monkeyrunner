from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice
from subprocess import call

class Utility:
    def __init__(self):
        self.load = {}
        call(["adb", "devices"])
        print 'waitting for connection'
        self.device = MonkeyRunner.waitForConnection()
        self.height = float(self.device.getProperty('display.height'))
        self.width = float(self.device.getProperty('display.width'))

    def back(self, delay = 1):
        print 'back',
        self.device.press('KEYCODE_BACK', MonkeyDevice.DOWN_AND_UP)
        self.sleep(delay)

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
        pos = self.position(name)
        x = pos['x']
        y = pos['y']

        print 'click, %s (%d,%d)' %(name, x, y),
        self.device.touch(x, y, MonkeyDevice.DOWN_AND_UP)
        self.sleep(delay)

    def drag(self, **kwargs):
        print kwargs.msg
        self.device.drag(kwargs.start, kwargs.end, kwargs.duration, kwargs.steps)
        self.sleep(kwargs.delay)

    def hold(self, **args):
        name = args['name']
        pos = self.position(name)
        x = pos['x']
        y = pos['y']
        duration = args.get('duration', 1)
        steps = args.get('steps', 10)
        delay = args.get('delay', 1)

        print 'hold %s (%d, %d), %fs (%d)' %(name, x, y, duration, steps),
        self.device.drag((x,y), (x,y), duration, steps)
        self.sleep(delay)

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

        pos = self.position(name1)
        color = self.colors[name2]
        x = pos['x']
        y = pos['y']
        print 'pixel %s (%d, %d), %s ' %(name1, x, y, name2),

        if img == False:
            img = self.device.takeSnapshot()

        p = img.getRawPixel(x, y)
        print p
        return p == color
    def position(self, name):
        pos = self.positions[name]
        x = self.width * pos['x']
        y = self.height * pos['y']
        return {
            'x': int(x),
            'y': int(y),
        }

    def sleep(self, delay = 1):
        if not delay == 0:
            print 'wait %fs' %(delay)
            MonkeyRunner.sleep(delay)

class TapTitans:
    def __init__(self):
        self.util = Utility()
        self.device = self.util.device
        self.package = 'com.gamehivecorp.taptitans'
        self.activity = 'com.gamehivecorp.ghplugin.ImmersivePlayerNativeActivity'

        self.util.positions = {
            'fairy': { 'x': 0.5, 'y': 0.25 },
            'ad watch': { 'x': 0.6, 'y': 0.625 },
            'close': { 'x': 0.8825, 'y': 0.2 },
        }
        self.util.colors = {
            'ad': (-1,33,33,33),
        }

    def open(self):
        self.device.startActivity(component = self.package + '/' + self.activity)

    def play(self):
        self.open()
        i = 1 
        while i:
            current = self.device.getProperty('am.current.comp.class')
            print current

            i += 1
            if current == 'com.gamehivecorp.ghplugin.ImmersivePlayerNativeActivity':
                self.util.click('fairy', 0.1)
                self.util.click('close', 0.1)
                if i % 100 == 0 :
                    self.util.click('ad watch', 0.1)
                    i = 1
            elif current == 'com.android.launcher2.Launcher':
                i = 0
            else:
                self.util.sleep(40)
                self.util.back()
                self.open()
                self.util.sleep(10)

    def test(self):
        self.util.click('ad watch', 0.1)

self = TapTitans()
self.play()