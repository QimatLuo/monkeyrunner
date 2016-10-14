from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice

device = MonkeyRunner.waitForConnection()
activity = 'com.avalon.cave/org.cocos2dx.cpp.AppActivity'
#device.startActivity(component=activity); MonkeyRunner.sleep(10);

load_checkMark = MonkeyRunner.loadImageFromFile('./checkMark.png','png') 
load_gem = MonkeyRunner.loadImageFromFile('./gem.png','png') 
load_goOut = MonkeyRunner.loadImageFromFile('./goOut.png','png') 

def watchAd():
    device.touch(41,176, MonkeyDevice.DOWN_AND_UP); print 'click gem'; MonkeyRunner.sleep(1);
    device.touch(244,684, MonkeyDevice.DOWN_AND_UP); print 'click accept'; MonkeyRunner.sleep(1);
    device.touch(400,670, MonkeyDevice.DOWN_AND_UP); print 'click second accept'; MonkeyRunner.sleep(1);

    print 'wait 18'
    MonkeyRunner.sleep(18)
    
    device.press("KEYCODE_BACK", MonkeyDevice.DOWN_AND_UP); print 'back'; MonkeyRunner.sleep(3);




while True:
    print 'take snapshot'
    img = device.takeSnapshot()
    img.writeToFile('./1.png')
    if (img.getSubImage((159,587,481,109)).sameAs(load_goOut, 0.6)):
        print 'Find goOut dialog, back then watch Ad'
        device.press("KEYCODE_BACK", MonkeyDevice.DOWN_AND_UP); MonkeyRunner.sleep(3);
        watchAd()
    elif (img.getSubImage((378,661,43,29)).sameAs(load_checkMark, 0.6)):
        print 'Find check mark, click then watch Ad'
        device.touch(378,661, MonkeyDevice.DOWN_AND_UP); print 'click check mark'; MonkeyRunner.sleep(1);
        watchAd()
    elif (img.getSubImage((41,176,42,21)).sameAs(load_gem, 0.4)):
        print 'Find gem, just watch Ad'
        watchAd()
    elif True:
        print 'Not found, try again'
        MonkeyRunner.sleep(1)
        device.press("KEYCODE_BACK", MonkeyDevice.DOWN_AND_UP); print 'back'; MonkeyRunner.sleep(3);
