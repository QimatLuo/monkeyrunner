import copy
import os
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
            'close pause': { 'x': 0.89375, 'y': 0.2953125 },
            'done': { 'x': 0.515, 'y': 0.9375 },
            'lose': { 'x': 0.325, 'y': 0.58203125 },
            'lose ok': { 'x': 0.5, 'y': 0.58203125 },
            'no': { 'x': 0.3125, 'y': 0.6640625 },
            'pause': { 'x': 0.1, 'y': 0.01 },
            'stage': { 'x': 0.0525, 'y': 0.16 },
            'step1': { 'x': 0.5, 'y': 0.6875 },
            'step2': { 'x': 0.25, 'y': 0.296875 },
            'step3': { 'x': 0.7125, 'y': 0.69375 },
            'step4': { 'x': 0.5, 'y': 0.8203125 },
            'step5': { 'x': 0.69375, 'y': 0.5625 },
            'title ok': { 'x': 0.5, 'y': 0.625 },
            'title': { 'x': 0.095, 'y': 0.5 },
            'upgrade': { 'x': 0.7, 'y': 0.34 },
        }
        self.util.colors = {
            'close pause': (-1,255,255,254),
            'done': (-1,255,255,255),
            'done disabled': (-1,127,127,127),
            'lose': (-1,255,255,255),
            'pause': (-1,211,143,40),
            'stage': (-1,255,255,255),
            'title': (-1,207,201,139),
        }

        for y in range(5):
            for x in range(5):
                self.util.positions[str(x) + str(y)] = {
                    'x': 0.19 + 0.15 * x,
                    'y': 0.53 + 0.1 * y,
                }

        self.pawn = {}
        path = 'sample/'
        for name in os.listdir(path):
            self.pawn[name[0:-4]] = open(path + name, 'r').read().split('\n')

        self.reset()

    def get(self, x, y, img):
        pawn = self.board[y][x]
        if len(pawn) < 100:
            pos = self.util.position(str(x) + str(y))
            i = img.getRawPixelInt(pos['x'], pos['y'])
            if -10406319 >= i and i >= -10603443 and y < 3:
                return True
            else:
                return False

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

    def isAble(self, x, y, name):
        if x < 0 or x > 4:
            return False

        if y < 0 or y > 4:
            return False

        try:
            pawn = self.board[y][x]
        except Exception, e:
            return False

        if type(pawn) is bool:
            return str(x) + str(y)

        if '_' in pawn and '_' in name:
            return False

        return str(x) + str(y)

    def isCorvered(self, target):
        for xy in self.team:
            x = int(xy[0])
            y = int(xy[1])
            able = self.move(xy, self.board[y][x])
            if target in able:
                return True

    def linearCheck(self, a, b):
        ax = int(a[0])
        ay = int(a[1])
        name = self.board[ay][ax]
        if not (name == 'hisha' or name == 'ryuo' or name == 'kakugyo' or name == 'ryuma' or name == 'kyosha'):
            return True

        bx = int(b[0])
        by = int(b[1])
        ix = 1 if ax < bx else -1
        iy = 1 if ay < by else -1

        if ax == bx:
            loop = True
            while loop:
                ay += iy

                if ay == by:
                    loop = False
                elif not type(self.board[ay][ax]) is bool:
                    return False
        elif ay == by:
            loop = True
            while loop:
                ax += ix

                if ax == bx:
                    loop = False
                elif not type(self.board[ay][ax]) is bool:
                    return False
        else:
            loop = True
            while loop:
                ax += ix
                ay += iy

                if ax == bx and ay == by:
                    loop = False
                elif not type(self.board[ay][ax]) is bool:
                    return False
        return True

    def move(self, xy, name, reverse = False):
        reverse = -1 if reverse else 1

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
                [-1, -2],
                [1, -2],
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
            ans = self.isAble(x, y, name)
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
        error = 0
        for y, row in enumerate(self.board):
            for x, col in enumerate(row):
                parse = self.get(x, y, img)
                self.board[y][x] = parse
                if parse == None:
                    error += 1
                elif type(parse) is bool:
                    self.emptySolt.append(str(x) + str(y))
                    continue
                elif parse == 'osho_':
                    self.osho = str(x) + str(y)
                elif '_' not in parse:
                    self.team.append(str(x) + str(y))

        if error == 1:
            call(['cp', '1.png', str(time.time()) + '.png'])
        else:
            return True

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
        self.board[4] = [[]]

        for y in range(h):
            row = []

            for x in range(w):
                row.append(self.pixelParse(x, y, sub))

            if len(''.join(row).replace('0', '')):
                self.board[4][0].append(row)

    def allCorvered(self, killer, targetAble):
        teamCorvered = []
        for xy in self.team:
            if xy == killer:
                continue
            x = int(xy[0])
            y = int(xy[1])
            teamCorvered.extend(self.move(xy, self.board[y][x]))

        x = int(killer[0])
        y = int(killer[1])
        name = self.board[y][x]
        kill = self.move(self.osho, name, True)
        print 'targetAble', targetAble
        print 'teamCorvered', teamCorvered
        for xy in kill:
            print 'kill:', xy
            killCorvered = self.move(xy, name)
            print 'killCorvered', killCorvered
            inter = set(teamCorvered + killCorvered) & set(targetAble)
            print 'test ANS:', xy, inter
            if len(inter) == len(targetAble):
                return xy

    def getAns(self, board):
        osho = None
        team = []
        empty = []

        for y, row in enumerate(board):
            for x, name in enumerate(row):
                obj = {
                    'x': x,
                    'y': y,
                    'xy': str(x) + str(y),
                    'name': name,
                }
                if name == 'osho_':
                    osho = obj
                elif type(name) is bool:
                    empty.append(obj)
                elif not '_' in name:
                    team.append(obj)
        require = [osho['xy']] + self.move(osho['xy'], osho['name'])
        xor = require
        for obj in team:
            able = self.move(obj['xy'], obj['name'])
            xor = set(xor) & set(able) ^ set(xor)
        if not len(xor):
            return True

    def test(self, img):
        if self.parsePawn(img):
            self.util.click('close pause')
            hand = self.board[4][0]
            if type(hand) is bool:
                array = self.team
            else:
                array = ['04']

            for oxy in array:
                ox = int(oxy[0])
                oy = int(oxy[1])
                oname = self.board[oy][ox]
                able = self.move(oxy, oname)

                for txy in able:
                    tx = int(txy[0])
                    ty = int(txy[1])
                    board = copy.deepcopy(self.board)
                    if txy == '04':
                        board[ty][tx] = oname
                    else:
                        board[ty][tx] = self.upgrade(txy, oname)
                    board[oy][ox] = False
                    if self.getAns(board):
                        print oxy,'to', txy
                        for xy in self.team:
                            x = int(xy[0])
                            y = int(xy[1])
                            name = self.board[y][x]
                            if xy == txy:
                                continue
                            cover = self.move(xy, name)
                            print name, cover
                            if txy in cover:
                                self.util.click(oxy)
                                self.util.click(txy)
                                self.util.click('upgrade')
                                return
                        
        return
        print self.board
        print 'target:', self.osho
        king = [self.osho] + self.move(self.osho, 'osho_')
        print 'target move:', king
        hand = self.board[4][0]
        ans = None

        if type(hand) is bool:
            array = self.team
        else:
            array = ['04']

        for xy in array:
            x = int(xy[0])
            y = int(xy[1])
            name = self.board[y][x]
            print name, x, y

            print self.allCorvered(xy, king)

            kill = self.move(self.osho, name, True)
            print 'kill:', kill

            able = self.move(xy, name)
            if not able:
                continue
            print 'able:', able
            if type(hand) is bool:
                for xy in able:
                    name = self.upgrade(xy, name)
                    if self.osho in self.move(xy, name):
                        print 'add kill', xy
                        kill.append(xy)

            if not kill:
                continue
            inter = set(kill) & set(king) & set(able)
            print 'inter:',  inter
            for ans in list(inter):
                if (not type(hand) is bool) or self.linearCheck(str(x) + str(y), ans):
                    self.util.click(str(x) + str(y))
                    self.util.click(ans)
                    self.util.click('upgrade')
                    return True

    def upgrade(self, xy, name):
        x = int(xy[0])
        y = int(xy[1])
        if not self.board[y][x] == True:
            return name

        if name == 'hisha':
            return 'ryuo'
        elif name == 'kakugyo':
            return 'ryuma'
        else:
            return 'kinsho'


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
        print 'takeSnapshot...'
        img = self.device.takeSnapshot()
        if self.util.pixel('pause', img):
            self.util.click('pause')
            img.writeToFile('./1.png')
            if self.test(img):
                self.util.sleep(8)
            else:
                img.writeToFile('./2.png')
                self.util.sleep(1)
            self.reset()
        elif self.util.pixel('close pause', img):
            self.util.click('close pause')
        elif self.util.pixel('done', img):
            self.util.click('done')
        elif self.util.pixel('done', 'done disabled', img):
            self.util.click('no')
            self.util.click('done')
        elif self.util.pixel('title', img):
            self.util.click('title ok')
        elif self.util.pixel('lose', img):
            self.util.click('lose')
            self.util.click('lose ok')
        elif self.util.pixel('stage', img):
            self.util.click('step1', 2)
            self.util.click('step2', 2)
            self.util.click('step2', 2)
            self.util.click('step3', 2)
            self.util.click('step4', 2)
            self.util.click('step5', 2)

        current = self.device.getProperty('am.current.comp.class')
