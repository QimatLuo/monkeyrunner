from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice
print 'wheel.py'
import datetime
import sys 
from reset import Reset
reset = Reset()
device = reset.device

load_300gem = MonkeyRunner.loadImageFromFile('./300gem.png','png') 
load_again = MonkeyRunner.loadImageFromFile('./again.png','png') 
load_done = MonkeyRunner.loadImageFromFile('./done.png','png') 
load_uploaded = MonkeyRunner.loadImageFromFile('./uploaded.png','png') 

def uploadRecord(device):
    device.touch(700,1200, MonkeyDevice.DOWN_AND_UP); print 'click bag'; MonkeyRunner.sleep(1);
    device.touch(600,1200, MonkeyDevice.DOWN_AND_UP); print 'click setting'; MonkeyRunner.sleep(1);
    device.touch(300,700, MonkeyDevice.DOWN_AND_UP); print 'confirm'; MonkeyRunner.sleep(1);
    device.touch(300,700, MonkeyDevice.DOWN_AND_UP); print 'confirm 2'; MonkeyRunner.sleep(7);
    loop = True
    while loop:
        print 'check uploaded'
        img = device.takeSnapshot()
        if (img.getSubImage((300,588,200,111)).sameAs(load_uploaded, 0.8)):
            loop = False
            device.touch(400,666, MonkeyDevice.DOWN_AND_UP); print 'confirm'; MonkeyRunner.sleep(1);
            device.press('KEYCODE_BACK', MonkeyDevice.DOWN_AND_UP); print 'back'; MonkeyRunner.sleep(1);

def checkResult(device):
    print 'check result'
    img = device.takeSnapshot()
    sub = img.getSubImage((395,540,5,5))
    if (sub.sameAs(load_300gem, 0.3)):
        print '300 Gem'
    elif (sub.sameAs(load_again, 0.3)):
        print 'Again'
        device.touch(600,950, MonkeyDevice.DOWN_AND_UP); print 'get result'; MonkeyRunner.sleep(1);
        device.touch(600,950, MonkeyDevice.DOWN_AND_UP); print 'get result2'; MonkeyRunner.sleep(1);
        device.touch(400,730, MonkeyDevice.DOWN_AND_UP); print 'get result2'; MonkeyRunner.sleep(1);
        device.press('KEYCODE_BACK', MonkeyDevice.DOWN_AND_UP); print 'back'; MonkeyRunner.sleep(1);
        uploadRecord(device)
        swipeWheel(device)
        return checkResult(device)
    else:
        img.writeToFile('./' + datetime.datetime.now().strftime("%Y%m%d%H%M%S") + '.png')
        return True

def checkAgain(device):
    print 'check again'
    img = device.takeSnapshot()
    if (img.getSubImage((477,1040,66,33)).sameAs(load_done, 0.9)):
        sys.exit(0)
    else:
        device.touch(400,1050, MonkeyDevice.DOWN_AND_UP); print 'play again'; MonkeyRunner.sleep(5);


def swipeWheel(device):
    device.touch(640,830, MonkeyDevice.DOWN_AND_UP); print 'click wheel'; MonkeyRunner.sleep(5);
    checkAgain(device)
    device.drag((120,450),(810,450),0.15,1); print 'swipe wheel';
    MonkeyRunner.sleep(10)

play = True
while play:
    reset.resetGame(device)
    device.drag((700,555),(100,555),0.1,1); print 'swipe left'; MonkeyRunner.sleep(1);
    swipeWheel(device)
    play = checkResult(device)
