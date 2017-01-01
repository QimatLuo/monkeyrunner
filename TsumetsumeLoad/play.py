import datetime
import sys
sys.path.insert(0, '..')
from utility import Utility
from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice

class TsumeTsumeLoad:
    def __init__(self):
        self.util = Utility()
        self.device = self.util.device
        self.package = 'jp.co.dig.tsumetsumelord'
        self.activity = 'com.unity3d.player.UnityPlayerActivity'

        self.util.positions = {
        }
        self.util.colors = {
        }

        self.pawn = {
            'fuhyo': open('fuhyo.txt', 'r').read().split('\n'),
            'fuhyo_': open('fuhyo_.txt', 'r').read().split('\n'),
            'ginsho': open('ginsho.txt', 'r').read().split('\n'),
            'ginsho_': open('ginsho_.txt', 'r').read().split('\n'),
            'hisha': open('hisha.txt', 'r').read().split('\n'),
            'hisha_': open('hisha_.txt', 'r').read().split('\n'),
            'kakugyo': open('kakugyo.txt', 'r').read().split('\n'),
            'kakugyo_': open('kakugyo_.txt', 'r').read().split('\n'),
            'keima': open('keima.txt', 'r').read().split('\n'),
            'keima_': open('keima_.txt', 'r').read().split('\n'),
            'kinsho': open('kinsho.txt', 'r').read().split('\n'),
            'kinsho_': open('kinsho_.txt', 'r').read().split('\n'),
            'kyosha': open('kyosha.txt', 'r').read().split('\n'),
            'kyosha_': open('kyosha_.txt', 'r').read().split('\n'),
            'osho_': open('osho_.txt', 'r').read().split('\n'),
            'ryuma': open('ryuma.txt', 'r').read().split('\n'),
            'ryuma_': open('ryuma_.txt', 'r').read().split('\n'),
            'ryuo': open('ryuo.txt', 'r').read().split('\n'),
            'ryuo_': open('ryuo_.txt', 'r').read().split('\n'),
        }

    def open(self, sleep = 1):
        print 'open app'
        self.device.startActivity(component = self.package + '/' + self.activity)
        self.util.sleep(sleep)

    def play(self):
        self.open()

    def board(self, img):
        x = 91
        y = 626
        w = 618
        h = 492
        sub = img.getSubImage((x, y, w, h))
        array = []
        origin = None

        for yi, y in enumerate(range(h)):
            row = []
            for x in range(w):
                i = sub.getRawPixelInt(x, y)
                p = sub.getRawPixel(x, y)
                #print '%s %d %d,%d' %(p, i, x, y)
                if reduce(lambda a, b: a + b, p[1:]) / len(p[1:]) < 10:
                    row.append('*')
                elif p[1] > p[2] and p[1] > p[3] and p[1] > 170 and p[2] > 170 and p[3] > 100: #general
                    row.append('+')
                else:
                    row.append(' ')

            array.append(row)
            if origin == None:
                try:
                    origin = [''.join(row).index('*     '), 0]
                    array = array[yi-1:]
                except:
                    origin = None

        return array

    def get(self, array, x, y):
        mapX = [
            [0, 123],
            [124, 247],
            [247, 370],
            [371, 494],
            [495, 618],
        ]

        mapY = [
            [0, 123],
            [123, 246],
            [246, 369],
            [368, 491],
        ]

        X = mapX[x]
        Y = mapY[y]

        for key, value in self.pawn.iteritems():
            error = 0
            for i, row in enumerate(array[Y[0]+7:Y[1]-11]):
                arr = []
                #print ''.join(row)[X[0]+3:X[1]-3]
                for j, col in enumerate(row[X[0]+3:X[1]-3]):
                    check = value[i][j] == col
                    if check:
                        arr.append('o')
                    else:
                        error += 1
                        arr.append(' ')
            if error < 2000:
                return key

    def test(self):
        img = self.device.takeSnapshot()
        img.writeToFile('./1.png')
        '''
        img = MonkeyRunner.loadImageFromFile('./1.png','png') 
        '''
        array = self.board(img)
        for y in range(4):
            row = []
            for x in range(5):
                row.append(self.get(array, x, y))
            print row

self = TsumeTsumeLoad()
self.test()
