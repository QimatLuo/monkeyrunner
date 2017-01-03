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
            'pause': (-1,211,143,40),
        }

        for y in range(5):
            for x in range(5):
                self.util.positions[str(x) + str(y)] = {
                    'x': 0.19 + 0.15 * x,
                    'y': 0.53 + 0.1 * y,
                }

        self.pawn = {
            'fuhyo': open('sample/fuhyo.txt', 'r').read().split('\n'),
            'fuhyo_': open('sample/fuhyo_.txt', 'r').read().split('\n'),
            'ginsho': open('sample/ginsho.txt', 'r').read().split('\n'),
            'ginsho_': open('sample/ginsho_.txt', 'r').read().split('\n'),
            'hisha': open('sample/hisha.txt', 'r').read().split('\n'),
            'hisha_': open('sample/hisha_.txt', 'r').read().split('\n'),
            'kakugyo': open('sample/kakugyo.txt', 'r').read().split('\n'),
            'kakugyo2': open('sample/kakugyo2.txt', 'r').read().split('\n'),
            'kakugyo_': open('sample/kakugyo_.txt', 'r').read().split('\n'),
            'keima': open('sample/keima.txt', 'r').read().split('\n'),
            'keima_': open('sample/keima_.txt', 'r').read().split('\n'),
            'kinsho': open('sample/kinsho.txt', 'r').read().split('\n'),
            'kinsho_': open('sample/kinsho_.txt', 'r').read().split('\n'),
            'kyosha': open('sample/kyosha.txt', 'r').read().split('\n'),
            'kyosha_': open('sample/kyosha_.txt', 'r').read().split('\n'),
            'osho_': open('sample/osho_.txt', 'r').read().split('\n'),
            'ryuma': open('sample/ryuma.txt', 'r').read().split('\n'),
            'ryuma_': open('sample/ryuma_.txt', 'r').read().split('\n'),
            'ryuo': open('sample/ryuo.txt', 'r').read().split('\n'),
            'ryuo_': open('sample/ryuo_.txt', 'r').read().split('\n'),
            'ryuo_2': open('sample/ryuo_2.txt', 'r').read().split('\n'),
        }

        self.reset()

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

            if error < 1700:
                return re.sub('\d', '', key)

    def isAble(self, x, y):
        if x < 0 or x > 4:
            return False

        if y < 0 or y > 4:
            return False

        try:
            pawn = self.board[y][x]
        except Exception, e:
            return False

        if pawn == '' or pawn == 'osho_':
            return str(x) + str(y)

    def move(self, xy, name):
        if name == 'osho_':
            reverse = 1
        else:
            reverse = -1

        target = [int(xy[0]), int(xy[1])]
        able = []

        if xy == '04':
            return self.emptySolt

        if name == 'osho_':
            possible = [
                [-1, -1],
                [-1, 0],
                [-1, 1],
                [0, -1],
                [0, 1],
                [1, -1],
                [1, 0],
                [1, 1],
                [-1, 2],
                [1, 2],
            ]
        elif name == 'fuhyo':
            possible = [
                [0, -1],
            ]
        elif name == 'ginsho':
            possible = [
                [-1, -1],
                [-1, 1],
                [0, -1],
                [1, -1],
                [1, 1],
            ]
        elif name == 'hisha':
            possible = [
                [-1, 0],
                [0, -1],
                [0, 1],
                [1, 0],
                [-2, 0],
                [-3, 0],
                [-4, 0],
                [0, -2],
                [0, -3],
                [0, 2],
                [0, 3],
                [2, 0],
                [3, 0],
                [4, 0],
            ]
        elif name == 'kakugyo':
            possible = [
                [-1, -1],
                [-1, 1],
                [1, -1],
                [1, 1],
                [-2, -2],
                [-3, -3],
                [-2, 2],
                [-3, 3],
                [2, -2],
                [3, -3],
                [2, 2],
                [3, 3],
            ]
        elif name == 'keima':
            possible = [
                [-1, 2],
                [1, 2],
            ]
        elif name == 'kinsho':
            possible = [
                [-1, -1],
                [-1, 0],
                [0, -1],
                [0, 1],
                [1, -1],
                [1, 0],
            ]
        elif name == 'kyosha':
            possible = [
                [0, -1],
                [0, -2],
                [0, -3],
            ]
        elif name == 'ryuma':
            possible = [
                [-1, -1],
                [-1, 0],
                [-1, 1],
                [0, -1],
                [0, 1],
                [1, -1],
                [1, 0],
                [1, 1],
                [-2, -2],
                [-3, -3],
                [-2, 2],
                [-3, 3],
                [2, -2],
                [3, -3],
                [2, 2],
                [3, 3],
            ]
        elif name == 'ryuo':
            possible = [
                [-1, -1],
                [-1, 0],
                [-1, 1],
                [0, -1],
                [0, 1],
                [1, -1],
                [1, 0],
                [1, 1],
                [-2, 0],
                [-3, 0],
                [-4, 0],
                [0, -2],
                [0, -3],
                [0, 2],
                [0, 3],
                [2, 0],
                [3, 0],
                [4, 0],
            ]
        else:
            return False

        for xy in possible:
            x = target[0] + xy[0] * reverse
            y = target[1] + xy[1] * reverse
            ans = self.isAble(x, y)
            if ans:
                able.append(ans)
        return able

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
                elif parse == '':
                    self.emptySolt.append(str(x) + str(y))
                    continue
                elif parse == 'osho_':
                    self.osho = str(x) + str(y)
                elif '_' not in parse:
                    self.team.append(str(x) + str(y))

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

    def reset(self):
        self.board = [
            [[],[],[],[],[]],
            [[],[],[],[],[]],
            [[],[],[],[],[]],
            [[],[],[],[],[]],
            [[],[],[],[],[]],
        ]

        self.team = []
        self.emptySolt = []

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
        print 'target:', self.osho
        self.util.click('close pause')
        hand = self.board[4][0]
        ans = None

        if hand == '':
            array = self.team
        else:
            array = ['04']

        for xy in array:
            x = int(xy[0])
            y = int(xy[1])

            kill = self.move(self.osho, self.board[y][x])
            if not kill:
                continue

            able = self.move(xy, self.board[y][x])
            if not able:
                continue

            king = self.move(self.osho, 'osho_')

            inter = set(kill) & set(king) & set(able)
            if len(inter):
                print self.board[y][x], x, y, kill
                print 'king:', king
                print 'inter:',  inter
                ans = list(inter)[0]
                self.util.click(str(x) + str(y))
                self.util.click(ans)
                self.util.click('upgrade')
                break

test = len(sys.argv) > 1
self = TsumeTsumeLoad(test)
if test:
    img = MonkeyRunner.loadImageFromFile('./1.png','png')
    print '<body style="margin:0;background:black;color:white;"><pre>'
    self.test(img)
    print '</pre></body>'
else:
    self.open()
    current = self.device.getProperty('am.current.comp.class')
    while  current == self.activity:
        img = self.device.takeSnapshot()
        if self.util.pixel('pause', img):
            self.util.click('pause')
            img.writeToFile('./1.png')
            self.test(img)
            self.reset()
            self.util.sleep(8)
        current = self.device.getProperty('am.current.comp.class')
