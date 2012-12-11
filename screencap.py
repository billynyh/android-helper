from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice, MonkeyImage
import datetime

DIR = "output/"

def capture_and_save(fname):
    device = MonkeyRunner.waitForConnection()
    snapshot = device.takeSnapshot()
    snapshot.writeToFile(DIR + fname)

def capture(prefix=""):
    d = datetime.datetime.now()
    fname = d.strftime("%Y%m%d-%H%M%S.png")
    if prefix:
        fname = prefix + fname
    capture_and_save(fname)

capture()
