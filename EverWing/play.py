import copy
import os
import time
import re
import sys
sys.path.insert(0, '..')
from utility import Utility
from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice
from subprocess import call

class EverWing:
    def __init__(self, noDevice = None):
        self.util = Utility(noDevice = None)
        self.device = self.util.device
        self.activity = 'com.unity3d.player.UnityPlayerActivity'

        self.util.mappings = {
            'stage finished': {
                'x': 0.33611111111111114,
                'y': 0.9403153153153153,
                'color': (-1, 252, 255, 255),
            },
            'trophies ad': {
                'x': 0.8416666666666667,
                'y': 0.8367117117117117,
                'color': (-1, 237, 6, 214),
            },
            'sidekicks ad': {
                'x': 0.15555555555555556,
                'y': 0.8130630630630631,
                #'color': (-1, 237, 6, 214),
                'color': (-1, 210, 18, 184),
            },
            'setting gear': {
                'x': 0.9259259259259259,
                'y': 0.11261261261261261,
                'color': (-1, 254, 254, 254),
            },
            'center ok': {
                'x': 0.5138888888888888,
                'y': 0.6475225225225225,
                'color': (-1, 252, 255, 255),
            },
            'bottom left ok': {
                'x': 0.18055555555555555,
                'y': 0.9420045045045045,
                'color': (-1, 252, 255, 255),
            },
            'score': {
                'x': 0.9537037037037037,
                'y': 0.11261261261261261,
                'color': (-1, 255, 254, 204),
            },
            'play': {
                'x': 0.5027777777777778,
                'y': 0.9121621621621622,
                'color': (-1, -1, -1, -1),
            },
            'no ad ok': {
                'x': 0.4111111111111111,
                'y': 0.6469594594594594,
                'color': (-1, 252, 255, 255),
            },
            'new quest': {
                'x': 0.6925925925925925,
                'y': 0.4144144144144144,
                'color': (-1, 248, 219, 5),
            },
            'quest': {
                'x': 0.812962962962963,
                'y': 0.42792792792792794,
                'color': (-1, -1, -1, -1),
            },
        }

    def open(self, sleep = 1):
        print 'open app'
        self.util.sleep(sleep)

    def clickBottomLeftOk(self, img):
        self.util.click('bottom left ok')

    def clickCenterOk(self, img):
        self.util.click('center ok')

    def clickGameFinishedButton(self, img):
        self.util.click('stage finished')

    def clickGetSidekicksAd(self, img):
        self.util.click('sidekicks ad')
        self.clickCenterOk(img)
        self.clickNoAdOk(img)
        self.clickPlay(img)

    def clickGetTrophiesAd(self, img):
        self.util.click('trophies ad')
        self.clickCenterOk(img)
        self.clickNoAdOk(img)
        self.clickPlay(img)

    def clickNoAdOk(self, img):
        self.util.click('no ad ok')

    def clickPlay(self, img):
        self.util.click('play')

    def clickQuest(self, img):
        self.util.click('quest')

    def hasBottomLeftOk(self, img):
        return self.util.pixel('bottom left ok', img)

    def hasCenterOk(self, img):
        return self.util.pixel('center ok', img)

    def hasNoAdOk(self, img):
        return self.util.pixel('no ad ok', img)

    def isGamePlaying(self, img):
        return self.util.pixel('score', img)

    def isGameFinished(self, img):
        return self.util.pixel('stage finished', img)

    def isHomePage(self, img):
        return self.util.pixel('setting gear', img)

    def isReadyToGetQuests(self, img):
        return self.util.pixel('new quest', img)

    def isReadyToGetSidekicks(self, img):
        return self.util.pixel('sidekicks ad', img)

    def isReadyToGetTrophies(self, img):
        return self.util.pixel('trophies ad', img)

    def play(self):
        while True:
            img = self.util.screenshot()
            img.writeToFile('1.png')
            print 'write img'
            if self.isHomePage(img):
                if self.isReadyToGetQuests(img):
                    self.clickQuest(img)
                elif self.isReadyToGetTrophies(img):
                    self.clickGetTrophiesAd(img)
                elif self.isReadyToGetSidekicks(img):
                    self.clickGetSidekicksAd(img)
                elif self.hasNoAdOk(img):
                    self.clickNoAdOk(img)
                else:
                    self.clickPlay(img)
            elif self.isGamePlaying(img):
                self.util.sleep(2)
            elif self.isGameFinished(img):
                self.clickGameFinishedButton(img)
            elif self.hasBottomLeftOk(img):
                self.clickBottomLeftOk(img)
            elif self.hasCenterOk(img):
                self.clickCenterOk(img)
            else:
                self.util.back()

test = len(sys.argv) > 1
self = EverWing(test)
if test:
    img = MonkeyRunner.loadImageFromFile('./1.png','png')
    if self.util.pixel('stage finished', img):
        print 'yes'
else:
    self.play()
'''
'''
