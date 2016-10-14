from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice

device = MonkeyRunner.waitForConnection()
activity = 'com.avalon.cave/org.cocos2dx.cpp.AppActivity'
#device.startActivity(component=activity); MonkeyRunner.sleep(10);

load_checkMark = MonkeyRunner.loadImageFromFile('./checkMark.png','png') 
load_gem = MonkeyRunner.loadImageFromFile('./gem.png','png') 
load_goOut = MonkeyRunner.loadImageFromFile('./goOut.png','png') 

def watchAd():
    device.touch(33,222, MonkeyDevice.DOWN_AND_UP); print 'click gem'; MonkeyRunner.sleep(1);
    device.touch(450,1034, MonkeyDevice.DOWN_AND_UP); print 'click accept'; MonkeyRunner.sleep(1);
    device.touch(565,1000, MonkeyDevice.DOWN_AND_UP); print 'click second accept'; MonkeyRunner.sleep(1);

    device.touch(33,222, MonkeyDevice.DOWN_AND_UP); print 'click gem'; MonkeyRunner.sleep(1);
    device.touch(450,1034, MonkeyDevice.DOWN_AND_UP); print 'click accept'; MonkeyRunner.sleep(1);
    device.touch(565,1000, MonkeyDevice.DOWN_AND_UP); print 'click second accept'; MonkeyRunner.sleep(1);
    print 'wait 18'
    MonkeyRunner.sleep(18)
    
    device.press("KEYCODE_BACK", MonkeyDevice.DOWN_AND_UP); print 'back'; MonkeyRunner.sleep(3);




while True:
    print 'take snapshot'
    img = device.takeSnapshot()
    img.writeToFile('./1.png')
    if (img.getSubImage((210,870,666,180)).sameAs(load_goOut, 0.6)):
        print 'Find goOut dialog, back then watch Ad'
        device.press("KEYCODE_BACK", MonkeyDevice.DOWN_AND_UP); MonkeyRunner.sleep(3);
        watchAd()
    elif (img.getSubImage((504,987,69,54)).sameAs(load_checkMark, 0.6)):
        print 'Find check mark, click then watch Ad'
        device.touch(504,987, MonkeyDevice.DOWN_AND_UP); print 'click check mark'; MonkeyRunner.sleep(1);
        watchAd()
    elif (img.getSubImage((33,222,66,33)).sameAs(load_gem, 0.6)):
        print 'Find gem, just watch Ad'
        watchAd()
    elif True:
        print 'Not found, try again'
        MonkeyRunner.sleep(1)
        device.press("KEYCODE_BACK", MonkeyDevice.DOWN_AND_UP); print 'back'; MonkeyRunner.sleep(3);
