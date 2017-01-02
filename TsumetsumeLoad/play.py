import time
import re
import sys
sys.path.insert(0, '..')
from utility import Utility
from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice
from subprocess import call

def bin(x):
    """
    bin(number) -> string

    Stringifies an int or long in base 2.
    """
    if x < 0: 
        return '-' + bin(-x)
    out = []
    if x == 0: 
        out.append('0')
    while x > 0:
        out.append('01'[x & 1])
        x >>= 1
        pass
    try: 
        return '0b' + ''.join(reversed(out))
    except NameError, ne2: 
        out.reverse()
    return '0b' + ''.join(out)

class TsumeTsumeLoad:
    def __init__(self, noDevice = None):
        self.util = Utility(noDevice = None)
        self.device = self.util.device
        self.package = 'jp.co.dig.tsumetsumelord'
        self.activity = 'com.unity3d.player.UnityPlayerActivity'

        self.util.positions = {
            'close pause': { 'x': 0.9, 'y': 0.3 },
            'pause': { 'x': 0.1, 'y': 0.01 },
            'upgrade': { 'x': 0.7, 'y': 0.34 },
        }
        self.util.colors = {
        }

        for y in range(5):
            for x in range(5):
                self.util.positions[str(x) + str(y)] = {
                    'x': 0.19 + 0.15 * x,
                    'y': 0.53 + 0.1 * y,
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

        self.board = [
            [[],[],[],[],[]],
            [[],[],[],[],[]],
            [[],[],[],[],[]],
            [[],[],[],[],[]],
            [[],[],[],[],[]],
        ]

    def get(self, x, y):
        pawn = self.board[y][x]
        if len(pawn) < 100:
            return ''

        '''
        print x,y
        for row in pawn:
            print ''.join(row)
        '''

        for key, value in self.pawn.iteritems():
            error = 0
            minLen = min(len(pawn), len(value) - 1)

            for i in range(minLen):
                xor = int(''.join(pawn[i]), 2) ^ int(''.join(value[i]), 2)
                error += len(re.sub('[^1]', '', bin(xor)))

            if error < 1600:
                return key

    def isAble(self, x, y):
        if x < 0 or x > 4:
            return False

        if y < 0 or y > 4:
            return False

        try:
            if self.board[y][x] == '':
                return str(x) + str(y)
        except Exception, e:
            return False

    def open(self, sleep = 1):
        print 'open app'
        self.device.startActivity(component = self.package + '/' + self.activity)
        self.util.sleep(sleep)

    def parsePawn(self, img):
        self.setBoard(img)
        self.setHand(img)
        for y, row in enumerate(self.board):
            for x, col in enumerate(row):
                parse = self.get(x, y)
                self.board[y][x] = parse
                if parse == None:
                    call(['cp', '1.png', str(time.time()) + '.png'])

    def pixelParse(self, x, y, sub):
        i = sub.getRawPixelInt(x, y)
        p = sub.getRawPixel(x, y)
        #print '%s %d %d,%d' %(p, i, x, y)
        if reduce(lambda a, b: a + b, p[1:]) / len(p[1:]) < 10:
            return '1'
        elif p[1] > p[2] and p[1] > p[3] and p[1] > 170 and p[2] > 170 and p[3] > 100: #general
            return '1'
        else:
            return '0'

    def play(self):
        self.open()

    def setBoard(self, img):
        x = 91
        y = 626
        w = 618
        h = 492
        sub = img.getSubImage((x, y, w, h))
        origin = None
        size = 123
        shiftX = [0, 1, 1, 2, 3]

        for y in range(h):
            row = []
            for x in range(w):
                row.append(self.pixelParse(x, y, sub))

            if origin == None:
                try:
                    ''.join(row).index('1000000000000000000000000000') #try this
                    origin = y - 1
                except:
                    origin = None
            else:
                boardY = (y - origin - 1) / size
                for boardX in range(5):
                    pos = size * boardX + shiftX[boardX]
                    section = row[pos + 3:pos + size - 3]
                    if len(''.join(section).replace('0', '')):
                        self.board[boardY][boardX].append(section)

    def setHand(self, img):
        x = 73
        y = 1145
        w = 117
        h = 117
        sub = img.getSubImage((x, y, w, h))
        sub.writeToFile('./sub.png')
        self.board[4] = [[]]

        for y in range(h):
            row = []

            for x in range(w):
                row.append(self.pixelParse(x, y, sub))

            if len(''.join(row).replace('0', '')):
                self.board[4][0].append(row)

    def test(self, img):
        self.parsePawn(img)
        print self.board
        target = None
        for y in range(4):
            for x in range(5):
                if self.board[y][x] == 'osho_':
                    target = [x, y]
                    break
            if target:
                break
        print target
        self.util.click('close pause')
        hand = self.board[4][0]
        ans = None

        possible = []
        for y in range(3):
            y-= 1
            for x in range(3):
                x -= 1
                x = target[0] + x
                y = target[1] + y
                if self.isAble(x, y):
                    possible.append([x, y])
        print possible

        if hand == '':
            x = possible[0][0]
            y = possible[0][1]
            ans = self.isAble(x, y)
            self.util.click(ans)
            self.util.click('upgrade')
        else:
            self.util.click('04')
            if hand == 'kakugyo':
                for y in [-1, 1]:
                    for x in [-1, 1]:
                        x = target[0] + x
                        y = target[1] + y
                        ans = self.isAble(x, y)
                        if ans:
                            self.util.click(ans)
            elif hand == 'keima':
                for x in [-1, 1]:
                    x = target[0] + x
                    y = target[1] + 2
                    ans = self.isAble(x, y)
                    if ans:
                        self.util.click(ans)
            else:
                x = target[0]
                y = target[1] + 1
                ans = self.isAble(x, y)
                if not ans:
                    x = possible[0][0]
                    y = possible[0][1]
                    ans = self.isAble(x, y)

                self.util.click(ans)


test = len(sys.argv) > 1
self = TsumeTsumeLoad(test)
if test:
    img = MonkeyRunner.loadImageFromFile('./1.png','png')
else:
    img = self.device.takeSnapshot()
    self.util.click('pause')
    img.writeToFile('./1.png')

print '<body style="margin:0;background:black;color:white;"><pre>'
self.test(img)
print '</pre></body>'
