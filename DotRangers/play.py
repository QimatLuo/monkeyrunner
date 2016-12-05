import sys
sys.path.insert(0, '..')
from utility import Utility

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
