import sys
sys.path.insert(0, '..')
from utility import Utility

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
