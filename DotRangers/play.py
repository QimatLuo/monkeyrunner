import sys
sys.path.insert(0, '..')
from utility import Utility

class DotRangers:
    def __init__(self):
        self.util = Utility()
        self.device = self.util.device

        self.util.positions = {
            'ad': { 'x': 687, 'y': 685 },
            'ad yes': { 'x': 500, 'y': 530 },
        }
        self.util.colors = {
            'ad': (-1,33,33,33),
        }

    def watch(self):
        while (not self.util.pixel('ad')):
            print 'no'

self = DotRangers()
while True:
    self.watch()
    self.util.click('ad')
    self.util.click('ad yes')
    self.util.back()
