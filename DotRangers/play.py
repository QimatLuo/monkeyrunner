from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice
from subprocess import call

class Utility:
    def __init__(self):
        self.load = {}
        call(["adb", "devices"])
        print 'waitting for connection'
        self.device = MonkeyRunner.waitForConnection()

    def back(self, delay = 1):
        print 'back, wait %fs' %(delay)
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

        print 'click, %s (%d,%d), wait %fs' %(name, x, y, delay)
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

        print 'hold %s (%d, %d), %fs (%d), wait %fs' %(name, x, y, duration, steps, delay)
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
    def sleep(self, delay = 1):
        print 'wait %fs' %(delay)
        MonkeyRunner.sleep(delay)

class DotRangers:
    def __init__(self):
        self.util = Utility()
        self.device = self.util.device
        self.package = 'com.lv0.dotrangers'
        self.activity = 'com.unity3d.player.UnityPlayerActivity'

        self.util.positions = {
            'ad close': { 'x': 742, 'y': 62 },
            'ad yes': { 'x': 500, 'y': 530 },
            'ad': { 'x': 687, 'y': 685 },
            'close': { 'x': 460, 'y': 665 },
        }
        self.util.colors = {
            'ad': (-1,33,33,33),
        }

    def open(self):
        self.device.startActivity(component = self.package + '/' + self.activity)

    def play(self):
        self.open()
        loop = True
        while loop:
            current = self.device.getProperty('am.current.comp.class')
            print current

            if current == 'com.unity3d.player.UnityPlayerActivity':
                self.util.click('ad', 0.75)
                self.util.click('close', 0.75)
                self.util.click('ad yes', 0.75)
            elif current == 'com.unity3d.ads.android.view.UnityAdsFullscreenActivity':
                self.util.sleep(31)
                self.util.back()
                self.open()
            elif current == 'com.google.android.gms.ads.AdActivity':
                self.util.back()
                self.open()
            else:
                loop = False

    def watch(self):
        while (not self.util.pixel('ad')):
            print 'no'

self = DotRangers()
self.play()