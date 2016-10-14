from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice
import sys

device = MonkeyRunner.waitForConnection()
img = device.takeSnapshot()
#sub = img.getSubImage((sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4]))
sub = img.getSubImage((tuple(map(lambda x: int(x), sys.argv[1:5]))))
sub.writeToFile(sys.argv[5])
