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
            'activity': { 'x': 0.75, 'y': 0.2 },
            'close pause': { 'x': 0.89375, 'y': 0.2953125 },
            'done': { 'x': 0.515, 'y': 0.9375 },
            'friend1': { 'x': 0.25, 'y': 0.27 },
            'friend2': { 'x': 0.25, 'y': 0.37 },
            'friend3': { 'x': 0.25, 'y': 0.47 },
            'friend4': { 'x': 0.25, 'y': 0.57 },
            'friend5': { 'x': 0.25, 'y': 0.67 },
            'friend6': { 'x': 0.25, 'y': 0.77 },
            'lose': { 'x': 0.3025, 'y': 0.5859375 },
            'lose ok': { 'x': 0.5, 'y': 0.58203125 },
            'no': { 'x': 0.3125, 'y': 0.6640625 },
            'pause': { 'x': 0.1, 'y': 0.01 },
            'quest1': { 'x': 0.25, 'y': 0.3 },
            'quest2': { 'x': 0.25, 'y': 0.45 },
            'quest3': { 'x': 0.25, 'y': 0.6 },
            'stage': { 'x': 0.0525, 'y': 0.16 },
            'step1': { 'x': 0.5, 'y': 0.6875 },
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

    def isAble(self, x, y, name, board, cover):
        if x < 0 or x > 4:
            return False

        if y < 0 or y > 4:
            return False

        try:
            pawn = board[y][x]
        except Exception, e:
            return False

        if type(pawn) is bool:
            return 'empty'

        if not cover:
            if self.sameTeam(pawn, name):
                return False

        return pawn

    def move(self, xy, name, board, cover = False):
        reverse = 1
        pname = name
        if '_' in name:
            if not name == 'osho_':
                reverse = -1
                pname = name[0:-1]

        target = [int(xy[0]), int(xy[1])]
        able = []

        if xy == '04':
            return self.emptySolt

        if pname == 'osho_':
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
        elif pname == 'fuhyo':
            possible = [
                [0, -1],
            ]
        elif pname == 'ginsho':
            possible = [
                [-1, -1],
                [-1, 1],
                [0, -1],
                [1, -1],
                [1, 1],
            ]
        elif pname == 'hisha':
            i = 1
            pawn = True
            while pawn:
                x = target[0] + i * reverse
                y = target[1]
                pawn = self.isAble(x, y, name, board, cover)
                if pawn:
                    if pawn == 'empty' or pawn == 'osho_':
                        able.append(str(x) + str(y))
                        i += 1
                    else:
                        if self.sameTeam(pawn, name):
                            if cover:
                                able.append(str(x) + str(y))
                        else:
                            able.append(str(x) + str(y))
                        pawn = False
            i = -1
            pawn = True
            while pawn:
                x = target[0] + i * reverse
                y = target[1]
                pawn = self.isAble(x, y, name, board, cover)
                if pawn:
                    if pawn == 'empty' or pawn == 'osho_':
                        able.append(str(x) + str(y))
                        i -= 1
                    else:
                        if self.sameTeam(pawn, name):
                            if cover:
                                able.append(str(x) + str(y))
                        else:
                            able.append(str(x) + str(y))
                        pawn = False
            i = 1
            pawn = True
            while pawn:
                x = target[0]
                y = target[1] + i * reverse
                pawn = self.isAble(x, y, name, board, cover)
                if pawn:
                    if pawn == 'empty' or pawn == 'osho_':
                        able.append(str(x) + str(y))
                        i += 1
                    else:
                        if self.sameTeam(pawn, name):
                            if cover:
                                able.append(str(x) + str(y))
                        else:
                            able.append(str(x) + str(y))
                        pawn = False
            i = -1
            pawn = True
            while pawn:
                x = target[0]
                y = target[1] + i * reverse
                pawn = self.isAble(x, y, name, board, cover)
                if pawn:
                    if pawn == 'empty' or pawn == 'osho_':
                        able.append(str(x) + str(y))
                        i -= 1
                    else:
                        if self.sameTeam(pawn, name):
                            if cover:
                                able.append(str(x) + str(y))
                        else:
                            able.append(str(x) + str(y))
                        pawn = False
            return able
        elif pname == 'kakugyo':
            i = 1
            j = 1
            pawn = True
            while pawn:
                x = target[0] + i * reverse
                y = target[1] + j * reverse
                pawn = self.isAble(x, y, name, board, cover)
                if pawn:
                    if pawn == 'empty' or pawn == 'osho_':
                        able.append(str(x) + str(y))
                        i += 1
                        j += 1
                    else:
                        if self.sameTeam(pawn, name):
                            if cover:
                                able.append(str(x) + str(y))
                        else:
                            able.append(str(x) + str(y))
                        pawn = False
            i = -1
            j = -1
            pawn = True
            while pawn:
                x = target[0] + i * reverse
                y = target[1] + j * reverse
                pawn = self.isAble(x, y, name, board, cover)
                if pawn:
                    if pawn == 'empty' or pawn == 'osho_':
                        able.append(str(x) + str(y))
                        i -= 1
                        j -= 1
                    else:
                        if self.sameTeam(pawn, name):
                            if cover:
                                able.append(str(x) + str(y))
                        else:
                            able.append(str(x) + str(y))
                        pawn = False
            i = 1
            j = -1
            pawn = True
            while pawn:
                x = target[0] + i * reverse
                y = target[1] + j * reverse
                pawn = self.isAble(x, y, name, board, cover)
                if pawn:
                    if pawn == 'empty' or pawn == 'osho_':
                        able.append(str(x) + str(y))
                        i += 1
                        j -= 1
                    else:
                        if self.sameTeam(pawn, name):
                            if cover:
                                able.append(str(x) + str(y))
                        else:
                            able.append(str(x) + str(y))
                        pawn = False
            i = -1
            j = 1
            pawn = True
            while pawn:
                x = target[0] + i * reverse
                y = target[1] + j * reverse
                pawn = self.isAble(x, y, name, board, cover)
                if pawn:
                    if pawn == 'empty' or pawn == 'osho_':
                        able.append(str(x) + str(y))
                        i -= 1
                        j += 1
                    else:
                        if self.sameTeam(pawn, name):
                            if cover:
                                able.append(str(x) + str(y))
                        else:
                            able.append(str(x) + str(y))
                        pawn = False
            return able
        elif pname == 'keima':
            possible = [
                [-1, -2],
                [1, -2],
            ]
        elif pname == 'kinsho':
            possible = [
                [-1, -1],
                [-1, 0],
                [0, -1],
                [0, 1],
                [1, -1],
                [1, 0],
            ]
        elif pname == 'kyosha':
            i = -1
            pawn = True
            while pawn:
                x = target[0]
                y = target[1] + i * reverse
                pawn = self.isAble(x, y, name, board, cover)
                if pawn:
                    if pawn == 'empty' or pawn == 'osho_':
                        able.append(str(x) + str(y))
                        i -= 1
                    else:
                        if self.sameTeam(pawn, name):
                            if cover:
                                able.append(str(x) + str(y))
                        else:
                            able.append(str(x) + str(y))
                        pawn = False
            return able
        elif pname == 'ryuma':
            i = 1
            j = 1
            pawn = True
            while pawn:
                x = target[0] + i * reverse
                y = target[1] + j * reverse
                pawn = self.isAble(x, y, name, board, cover)
                if pawn:
                    if pawn == 'empty' or pawn == 'osho_':
                        able.append(str(x) + str(y))
                        i += 1
                        j += 1
                    else:
                        if self.sameTeam(pawn, name):
                            if cover:
                                able.append(str(x) + str(y))
                        else:
                            able.append(str(x) + str(y))
                        pawn = False
            i = -1
            j = -1
            pawn = True
            while pawn:
                x = target[0] + i * reverse
                y = target[1] + j * reverse
                pawn = self.isAble(x, y, name, board, cover)
                if pawn:
                    if pawn == 'empty' or pawn == 'osho_':
                        able.append(str(x) + str(y))
                        i -= 1
                        j -= 1
                    else:
                        if self.sameTeam(pawn, name):
                            if cover:
                                able.append(str(x) + str(y))
                        else:
                            able.append(str(x) + str(y))
                        pawn = False
            i = 1
            j = -1
            pawn = True
            while pawn:
                x = target[0] + i * reverse
                y = target[1] + j * reverse
                pawn = self.isAble(x, y, name, board, cover)
                if pawn:
                    if pawn == 'empty' or pawn == 'osho_':
                        able.append(str(x) + str(y))
                        i += 1
                        j -= 1
                    else:
                        if self.sameTeam(pawn, name):
                            if cover:
                                able.append(str(x) + str(y))
                        else:
                            able.append(str(x) + str(y))
                        pawn = False
            i = -1
            j = 1
            pawn = True
            while pawn:
                x = target[0] + i * reverse
                y = target[1] + j * reverse
                pawn = self.isAble(x, y, name, board, cover)
                if pawn:
                    if pawn == 'empty' or pawn == 'osho_':
                        able.append(str(x) + str(y))
                        i -= 1
                        j += 1
                    else:
                        if self.sameTeam(pawn, name):
                            if cover:
                                able.append(str(x) + str(y))
                        else:
                            able.append(str(x) + str(y))
                        pawn = False
            possible = [
                [-1, 0],
                [0, -1],
                [0, 1],
                [1, 0],
            ]
        elif pname == 'ryuo':
            i = 1
            pawn = True
            while pawn:
                x = target[0] + i * reverse
                y = target[1]
                pawn = self.isAble(x, y, name, board, cover)
                if pawn:
                    if pawn == 'empty' or pawn == 'osho_':
                        able.append(str(x) + str(y))
                        i += 1
                    else:
                        if self.sameTeam(pawn, name):
                            if cover:
                                able.append(str(x) + str(y))
                        else:
                            able.append(str(x) + str(y))
                        pawn = False
            i = -1
            pawn = True
            while pawn:
                x = target[0] + i * reverse
                y = target[1]
                pawn = self.isAble(x, y, name, board, cover)
                if pawn:
                    if pawn == 'empty' or pawn == 'osho_':
                        able.append(str(x) + str(y))
                        i -= 1
                    else:
                        if self.sameTeam(pawn, name):
                            if cover:
                                able.append(str(x) + str(y))
                        else:
                            able.append(str(x) + str(y))
                        pawn = False
            i = 1
            pawn = True
            while pawn:
                x = target[0]
                y = target[1] + i * reverse
                pawn = self.isAble(x, y, name, board, cover)
                if pawn:
                    if pawn == 'empty' or pawn == 'osho_':
                        able.append(str(x) + str(y))
                        i += 1
                    else:
                        if self.sameTeam(pawn, name):
                            if cover:
                                able.append(str(x) + str(y))
                        else:
                            able.append(str(x) + str(y))
                        pawn = False
            i = -1
            pawn = True
            while pawn:
                x = target[0]
                y = target[1] + i * reverse
                pawn = self.isAble(x, y, name, board, cover)
                if pawn:
                    if pawn == 'empty' or pawn == 'osho_':
                        able.append(str(x) + str(y))
                        i -= 1
                    else:
                        if self.sameTeam(pawn, name):
                            if cover:
                                able.append(str(x) + str(y))
                        else:
                            able.append(str(x) + str(y))
                        pawn = False
            possible = [
                [-1, -1],
                [-1, 1],
                [1, -1],
                [1, 1],
            ]
        else:
            return False

        for xy in possible:
            x = target[0] + xy[0] * reverse
            y = target[1] + xy[1] * reverse
            pawn = self.isAble(x, y, name, board, cover)
            if pawn:
                able.append(str(x) + str(y))
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
                else:
                    if parse == 'osho_':
                        self.osho = str(x) + str(y)
                    elif '_' not in parse:
                        self.team.append(str(x) + str(y))
                    else:
                        self.opponent.append(str(x) + str(y))

        if error == 1:
            call(['cp', '1.png', 'parse_' + time.strftime('%d_%H:%M:%S') + '.png'])
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
        self.opponent = []
        self.emptySolt = []

    def sameTeam(self, a, b):
        if not type(a) is str:
            return False

        if not type(b) is str:
            return False

        return not (int('_' in a) ^ int('_' in b))

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
        require = [osho['xy']] + self.move(osho['xy'], osho['name'], self.board)
        xor = require
        print 'require', require
        for obj in team:
            able = self.move(obj['xy'], obj['name'], board, True)
            xor = set(xor) & set(able) ^ set(xor)
            print obj['name'], able
            print xor
        if len(xor):
            return False

        return True

    def possibleTeam(self):
        if type(self.board[4][0]) is bool:
            array = self.team
        else:
            array = ['04']
        return array

    def checkmate(self, oxy, txy):
        self.util.click(oxy)
        self.util.click(txy)
        self.util.click('upgrade')

    def checkOsho(self, oxy, txy, board):
        print 'txy should in team cover:'
        if txy in self.move(self.osho, 'osho_', self.board):
            for xy in self.team:
                x = int(xy[0])
                y = int(xy[1])
                name = self.board[y][x]
                if xy == oxy:
                    continue
                cover = self.move(xy, name, board, True)
                print name, cover
                if (txy in cover):
                    return True
        else:
            tx = int(txy[0])
            ty = int(txy[1])
            name = board[ty][tx]
            if name == 'hisha' or name == 'ryuo' or name == 'kakugyo' or name == 'ryuma' or name == 'kyosha':
                return False
            else:
                return True

    def checkOpponents(self, oxy, txy, board):
        print 'txy dead should cover osho:'
        tx = int(txy[0])
        ty = int(txy[1])
        if len(self.opponent) == 0:
            return True

        safe = True
        for xy in self.opponent:
            x = int(xy[0])
            y = int(xy[1])
            name = self.board[y][x]
            able = self.move(xy, name, self.board)
            print name, able
            if txy in able:
                safe = False
                newBoard = copy.deepcopy(board)
                newBoard[y][x] = False
                newBoard[ty][tx] = name
                print newBoard
                for xy in self.team:
                    x = int(xy[0])
                    y = int(xy[1])
                    name = self.board[y][x]
                    if xy == oxy:
                        continue
                    cover = self.move(xy, name, newBoard, True)
                    print name, cover
                    if (self.osho in cover):
                        return True
        if safe:
            return True

    def test(self, img):
        if not self.parsePawn(img):
            return False

        self.util.click('close pause')

        for oxy in self.possibleTeam():
            ox = int(oxy[0])
            oy = int(oxy[1])
            oname = self.board[oy][ox]

            for txy in self.move(oxy, oname, self.board):
                print oxy, 'to', txy
                tx = int(txy[0])
                ty = int(txy[1])
                if not type(self.board[ty][tx]) is bool:
                    continue
                board = copy.deepcopy(self.board)
                if oxy == '04':
                    board[ty][tx] = oname
                else:
                    board[ty][tx] = self.upgrade(oxy, txy, oname)
                board[oy][ox] = False

                if not self.osho in self.move(txy, board[ty][tx], board):
                    continue

                print board

                if not self.getAns(board):
                    continue

                if not self.checkOsho(oxy, txy, board):
                    continue

                if not self.checkOpponents(oxy, txy, board):
                    continue

                self.checkmate(oxy, txy)
                return True
        call(['cp', '1.png', 'bug_' + time.strftime('%d_%H:%M:%S') + '.png'])
                        
    def upgrade(self, oxy, txy, name):
        y1 = int(oxy[1])
        y2 = int(txy[1])
        able = False
        for x in range(5):
            if (not y1 == 4) and (self.board[y1][x] == True):
                able = True
                break
            if (not y2 == 4) and (self.board[y2][x] == True):
                able = True
                break

        if not able or name == 'ryuo' or name == 'ryuma':
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
    start = time.time()
    play = 0
    stage = 1
    lose = 0
    combo = 0
    while  current == self.activity:
        print 'takeSnapshot...'
        img = self.device.takeSnapshot()
        if self.util.pixel('pause', img):
            self.util.click('pause')
            img.writeToFile('1.png')
            if self.test(img):
                play += 1
                print 'combo:', combo
                combo += 1
                self.util.sleep(6)
            else:
                self.util.sleep(1)
            self.reset()
        elif self.util.pixel('close pause', img):
            self.util.click('close pause')
        elif self.util.pixel('done', img):
            self.util.click('done', 2)
            self.util.click('done')
        elif self.util.pixel('done', 'done disabled', img):
            self.util.click('no')
            self.util.click('done')
        elif self.util.pixel('title', img):
            self.util.click('title ok')
        elif self.util.pixel('lose', img):
            lose += 1
            self.util.click('lose')
            self.util.click('lose ok')
            img.writeToFile('lose_' + time.strftime('%d_%H:%M:%S') + '.png')
        elif self.util.pixel('stage', img):
            stage += 1
            self.util.click('activity', 2)
            self.util.click('quest3', 2)
            self.util.click('friend6', 2)
            self.util.click('step3', 2)
            self.util.click('step4', 2)
            self.util.click('step5', 2)
            combo = 0

        current = self.device.getProperty('am.current.comp.class')
    end = time.time()
    print '     end:', time.localtime(end)
    print '   start:', time.localtime(start)
    print 'duration:', time.strftime('%H:%M:%S', time.gmtime(end - start))
    print '    play:', play
    print '   stage:', stage
    print '    each:', (play / stage)
    print '    lose:', lose
