import subprocess
import csv
import time, datetime
import MySQLdb as mdb
from PID import PID
# from ADDA import ADDA  # DAC interface by Chip lab. We should do our own.
##from setVoltage import SetVoltage
import setVoltage
import winsound
import atexit

import requests
import re
import os
import time


##import subprocess
##name = "WavemeterData.exe 3"
##test= subprocess.check_output(name)
##print test


name = "WavemeterData.exe "
name = name+str(3)
with open(os.devnull, "w") as fnull:
    test = subprocess.call(name, stdout = fnull)
waveOut = str(subprocess.check_output(name))
waveOut = waveOut.split(" ")
test = waveOut   
freq = [0,0,0]
freq[2] = float(waveOut[1])
##    print waveOut
freq[0] = float(waveOut[0])
freq[1] = float(waveOut[2])
j=0
