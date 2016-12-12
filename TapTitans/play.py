import datetime
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
            'skill1': { 'x': 0.1, 'y': 0.9 },
            'skill2': { 'x': 0.25, 'y': 0.9 },
            'skill3': { 'x': 0.4375, 'y': 0.9 },
            'skill4': { 'x': 0.5625, 'y': 0.9 },
            'skill5': { 'x': 0.75, 'y': 0.9 },
            'skill6': { 'x': 0.9, 'y': 0.9 },
            'ad close': { 'x': 0.85625, 'y': 0.1015625 },
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

            if current == 'com.gamehivecorp.ghplugin.ImmersivePlayerNativeActivity':
                self.util.click('fairy', 0.1)
                self.util.click('close', 0.1)
                if i % 300 == 0 :
                    self.util.click('ad watch', 0.1)
                    self.util.click('skill6', 0.1)
                    self.util.click('skill5', 0.1)
                    self.util.click('skill4', 0.1)
                    self.util.click('skill3', 0.1)
                    self.util.click('skill2', 0.1)
                    self.util.click('skill1', 0.1)
                    i = 1
                else:
                    i += 1
            elif current == 'com.android.launcher2.Launcher' or current == None:
                i = 0
                print datetime.datetime.now()
            else:
                self.util.sleep(40)
                self.util.back()
                self.open()
                self.util.sleep(10)
                self.util.click('ad close', 0.1)
                i = 300

    def test(self):
        self.util.click('ad watch', 0.1)

self = TapTitans()
self.play()
