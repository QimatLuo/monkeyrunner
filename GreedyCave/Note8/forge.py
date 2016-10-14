from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice
print 'forge.py'
import sys
import datetime
from reset import Reset
reset = Reset()
device = reset.device

load_MoLi1 = MonkeyRunner.loadImageFromFile('./MoLi1.png','png') 
load_MoLi2 = MonkeyRunner.loadImageFromFile('./MoLi2.png','png') 
load_MoLi3 = MonkeyRunner.loadImageFromFile('./MoLi3.png','png') 

def checkForge():
    print 'check forge'
    img = device.takeSnapshot()
    #img = img.getSubImage((414,130,94,26))
    #img = img.getSubImage((414,176,94,26))
    img = img.getSubImage((414,222,94,26))
    img.writeToFile('./' + datetime.datetime.now().strftime("%Y%m%d%H%M%S") + '.png')
    if (img.sameAs(load_MoLi3, 0.9)):
        print 'MoLi'
    else:
        return True

play = True
while play:
    reset.resetGame(device)
    device.drag((700,555),(100,555),0.1,1); print 'swipe left'; MonkeyRunner.sleep(1);
    device.drag((700,555),(100,555),0.1,1); print 'swipe left'; MonkeyRunner.sleep(1);
    device.touch(270,800, MonkeyDevice.DOWN_AND_UP); print 'click NPC'; MonkeyRunner.sleep(1);
    device.touch(200,700, MonkeyDevice.DOWN_AND_UP); print 'choice forge'; MonkeyRunner.sleep(1);
    device.touch(400,570, MonkeyDevice.DOWN_AND_UP); print 'confirm'; MonkeyRunner.sleep(1);
    device.drag((700,1050),(255,175)); print 'select item 1,7'; MonkeyRunner.sleep(1);
    #device.touch(400,140, MonkeyDevice.DOWN_AND_UP); print 'select attr 1'; MonkeyRunner.sleep(1);
    #device.touch(400,190, MonkeyDevice.DOWN_AND_UP); print 'select attr 2'; MonkeyRunner.sleep(1);
    device.touch(400,240, MonkeyDevice.DOWN_AND_UP); print 'select attr 3'; MonkeyRunner.sleep(1);
    device.touch(400,300, MonkeyDevice.DOWN_AND_UP); print 'forge'; MonkeyRunner.sleep(3);
    play = checkForge()
