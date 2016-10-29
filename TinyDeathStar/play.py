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

class TinyDeathStar:
    def __init__(self):
        self.util = Utility()
        self.device = self.util.device

        self.util.positions = {
            'floor': { 'x': 400, 'y': 800 },
            'imperial floor': { 'x': 400, 'y': 888 },
            'salvace droids': { 'x': 400, 'y': 900 },
            'elevator up': { 'x': 400, 'y': 800 },
            'elevator down': { 'x': 400, 'y': 1000 },
            'continue': { 'x': 400, 'y': 900 },
            'yes': { 'x': 555, 'y': 888 },
            'no': { 'x': 222, 'y': 888 },
            'roof': { 'x': 66, 'y': 22 },
            'free': { 'x': 111, 'y': 444 },
            'place order 1': { 'x': 444, 'y': 400 },
            'action': { 'x': 58, 'y': 1173 },
            'app': { 'x': 200, 'y': 1150 },
            'elevator empty': { 'x': 72, 'y': 1000 },
            'elevator target border 1': { 'x': 155, 'y': 765 },
            'elevator target border 2': { 'x': 155, 'y': 530 },
            'elevator target border 3': { 'x': 155, 'y': 305 },
            'elevator target border 4': { 'x': 155, 'y': 65 },
            'roof red light': { 'x': 258, 'y': 616 },
            'menu': { 'x': 799, 'y': 1279 },
            'menu modal': { 'x': 799, 'y': 1200 },
            'leave modal': { 'x': 730, 'y': 1234 },
            'leave': { 'x': 730, 'y': 1234 },
            'desktop': { 'x': 730, 'y': 1234 },
            'imperial item 1': { 'x': 444, 'y': 280 + 145 },
            'imperial item 2': { 'x': 444, 'y': 510 + 145 },
            'imperial border 1': { 'x': 444, 'y': 280 },
            'imperial border 2': { 'x': 444, 'y': 510 },
            'stock item 1': { 'x': 444, 'y': 255 + 145 },
            'stock item 2': { 'x': 444, 'y': 490 + 145 },
            'stock item 3': { 'x': 444, 'y': 720 + 145 },
            'stock border 1': { 'x': 444, 'y': 255 },
            'stock border 2': { 'x': 444, 'y': 490 },
            'stock border 3': { 'x': 444, 'y': 720 },
            'hero icon': { 'x': 144, 'y': 444 },
        }
        self.util.colors = {
            'continue': (-1,15,209,0),
            'elevator empty': (-1,26,27,31),
            'elevator empty imperial': (-1,11,1,2),
            'elevator target border': (-1,0,174,239),
            'elevator target border 4': (-1,0,174,238),
            'roof red light': (-1,255,0,0),
            'menu': (-1,27,88,22),
            'menu modal': (-1,34,53,15),
            'leave modal': (-1,56,58,58),
            'leave': (-1,241,250,251),
            'desktop': (-1,223,178,127),
            'item border green': (-1,98,255,50),
            'item border red': (-1,253,168,154),
            'hero icon': (-1,255,255,255),
        }

    def action_24hr(self):
        self.util.click('salvace droids')
        self.util.click('free', 4)
        self.util.back()
        return True

    def action_alert(self):
        self.util.click('floor')
        self.util.click('place order 1')
        return True

    def action_assicnments(self):
        self.util.click('floor')
        self.util.click('continue')
        self.util.back()
        return True

    def action_cargo(self):
        return True

    def action_elevator(self):
        self.util.click('elevator up')
        loop = True
        while loop:
            print 'check elevator target'
            img = self.device.takeSnapshot()

            if self.util.pixel('roof red light', img):
                self.util.hold(
                    name ='elevator down',
                    duration = 6,
                    steps = 1,
                    delay = 2,
                )
                loop = False
            else:
                for i in range(1,4):
                    if self.util.pixel('elevator target border %d' %(i), 'elevator target border', img):
                        loop = False
                        break
                if loop:
                    loop = not self.util.pixel('elevator target border 4', img)
                    i += 1

                self.util.hold(
                    name ='elevator up',
                    #duration = 0.6 * (i-1) + 0.7, # 2x
                    #duration = 0.3 * (i-1) + 0.7, # 3x
                    #duration = 0.25 * (i-1) + 0.45, # 4x
                    duration = 0.14 * (i-1) + 0.45, # 5x
                    steps = 1,
                    delay = 2,
                )

        MonkeyRunner.sleep(4)
        print 'check elevator gone'
        img = self.device.takeSnapshot()
        if self.util.pixel('elevator empty', img):
            return True
        elif self.util.pixel('elevator empty', 'elevator empty imperial', img):
            return True
        elif not self.util.pixel('menu', img):
            self.util.back()
            self.util.back()
            return True
        return self.action_elevator()

    def action_imperial(self):
        self.util.click('imperial floor')

        print 'check green items'
        img = self.device.takeSnapshot()
        checkPoints = [280,510]
        for i in range(1,3):
            if self.util.pixel('imperial border %d' %(i), 'item border green', img):
                self.util.click('imperial item %d' %(i))
                break

        print 'check red items'
        img = self.device.takeSnapshot()
        for i in range(1,3):
            if self.util.pixel('imperial border %d' %(i), 'item border red', img):
                self.util.click('imperial item %d' %(i), 2)
                break

        self.util.click('yes')
        return True

    def action_hero(self, wait = True):
        MonkeyRunner.sleep(1);
        self.util.click('yes')
        self.find_people()
        if wait:
            while not self.util.pixel('hero icon'):
                print 'wait for continue dialog'
            self.util.click('continue')

        return True

    def action_people(self):
        return self.action_hero(False)

    def action_stock(self):
        self.util.click('floor')
        self.util.click('floor', 2)

        print 'check red items'
        img = self.device.takeSnapshot()
        notFound = True
        for i in range(1,4):
            if self.util.pixel('stock border %d' %(i), 'item border red', img):
                self.util.click('stock item %d' %(i))
                notFound = False
                break

        if notFound and self.util.pixel('leave', img):
            self.util.back()
                
        return True

    def action_unknown(self):
        self.util.hold(
            name ='elevator up',
            duration = 8,
            steps = 1,
            delay = 5,
        )
        self.util.click('yes')
        return True

    def action_vip(self):
        self.util.click('no')
        return True
        self.util.click('yes')
        img = self.device.takeSnapshot()
        for name in ['bigSpender','celebrity','levelMover','recruitingOfficer','supplyOfficer','upgrader']:
            if self.util.check(name, (92,878,70,129), 1, img):
                break

        print name
        self.util.hold(
            name ='elevator down',
            duration = 6,
            steps = 1,
            delay = 2,
        )
        self.util.click('yes')
        if name == 'levelMover':
            self.util.click('no')
        return True

    def find_people(self):
        self.util.click('roof')

        loop = True
        while loop:
            self.util.click('floor', 1.5);
            self.util.click('continue', 1)
            loop = self.util.pixel('leave')
            if loop:
                self.device.drag((444,800),(444,655)); print 'swipe 1 floor'; MonkeyRunner.sleep(2);

    def parse_action(self):
        print 'parse action'
        ret = True
        noAction = True
        img = self.device.takeSnapshot()
        for name in ['24hr','alert','assicnments','cargo','elevator','hero','imperial','people','stock','unknown','vip']:
            if self.util.check(name, (18,1093,77,77), 0.2, img):
                print '------------------'
                noAction = False
                self.util.click('action')
                ret = getattr(self, 'action_%s' % name)()
                self.device.drag((444,800),(444,8),1,1); print 'swipe to bottom'; MonkeyRunner.sleep(2);
                break
        if noAction:
            if self.util.pixel('desktop', img):
                self.util.click('app')
            elif not self.util.pixel('menu', img):
                self.util.back()
            elif self.util.pixel('leave modal', img):
                self.util.back()
                self.util.back()
            elif self.util.pixel('continue', img):
                self.util.click('continue')
            elif self.util.pixel('menu modal', img):
                self.util.back()
                
        return ret

self = TinyDeathStar()
#self.action_elevator() """
self.device.drag((444,800),(444,8),1,1); print 'swipe to bottom'; MonkeyRunner.sleep(2);
while self.parse_action():
    print ''
