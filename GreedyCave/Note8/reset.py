from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice
print 'reset.py'

load_download = MonkeyRunner.loadImageFromFile('./download.png','png') 
load_main = MonkeyRunner.loadImageFromFile('./main.png','png') 
load_overwrite = MonkeyRunner.loadImageFromFile('./overwrite.png','png') 

class Reset:
    device = MonkeyRunner.waitForConnection()

    def checkApp(self, device):
        loop = True
        while loop:
            print 'check main'
            img = device.takeSnapshot()
            if (img.getSubImage((377,600,50,15)).sameAs(load_main, 0.6)):
                loop = False
                device.touch(400,1222, MonkeyDevice.DOWN_AND_UP); print 'start game'; MonkeyRunner.sleep(3);

    def checkDownload(self, device):
        loop = True
        while loop:
            print 'check download'
            img = device.takeSnapshot()
            if (img.getSubImage((60,585,680,111)).sameAs(load_download, 0.8)):
                loop = False

    def checkOverwrite(self, device):
        loop = True
        while loop:
            print 'check overwrite'
            img = device.takeSnapshot()
            if (img.getSubImage((0,555,800,160)).sameAs(load_overwrite, 0.7)):
                loop = False
                device.touch(300,666, MonkeyDevice.DOWN_AND_UP); print 'confirm'; MonkeyRunner.sleep(1);
                device.touch(400,666, MonkeyDevice.DOWN_AND_UP); print 'confirm'; MonkeyRunner.sleep(5);

    def resetGame(self, device):
        activity = 'com.android.systemui/.recent.RecentsActivity'
        device.startActivity(component=activity); MonkeyRunner.sleep(1);
        device.touch(600,915, MonkeyDevice.DOWN_AND_UP); print 'click app 2'; MonkeyRunner.sleep(2);
        device.touch(600,600, MonkeyDevice.DOWN_AND_UP); print 'clear data'; MonkeyRunner.sleep(2);
        device.touch(600,747, MonkeyDevice.DOWN_AND_UP); print 'confirm'; MonkeyRunner.sleep(1);
        activity = 'com.avalon.cave/org.cocos2dx.cpp.AppActivity'
        device.startActivity(component=activity); MonkeyRunner.sleep(1);
        MonkeyRunner.sleep(20)
        self.checkApp(device)
        device.touch(400,900, MonkeyDevice.DOWN_AND_UP); print 'new character'; MonkeyRunner.sleep(17);
        device.touch(400,1222, MonkeyDevice.DOWN_AND_UP); print 'start game'; MonkeyRunner.sleep(5);
        device.touch(700,1200, MonkeyDevice.DOWN_AND_UP); print 'click bag'; MonkeyRunner.sleep(1);
        device.touch(600,1200, MonkeyDevice.DOWN_AND_UP); print 'click setting'; MonkeyRunner.sleep(3);
        device.touch(600,700, MonkeyDevice.DOWN_AND_UP); print 'download'; MonkeyRunner.sleep(7);
        self.checkDownload(device)
        device.touch(222,666, MonkeyDevice.DOWN_AND_UP); print 'confirm'; MonkeyRunner.sleep(5);
        self.checkOverwrite(device)
        self.checkApp(device)
        MonkeyRunner.sleep(7)
