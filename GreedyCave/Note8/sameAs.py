from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice
import sys

a = MonkeyRunner.loadImageFromFile(sys.argv[1],'png') 
b = MonkeyRunner.loadImageFromFile(sys.argv[2],'png') 
print a.sameAs(b, float(sys.argv[3]))
