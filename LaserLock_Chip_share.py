#

from __future__ import print_function

import subprocess
import csv
import time, datetime
import MySQLdb as mdb
#import pymysql
from PID import PID
from ADDA import ADDA  # DAC interface by Chip lab. We should do our own.
# import setVoltage
# import winsound
import atexit
import numpy as np
import requests
import re
import os
import time
#import wx



def getChannels():
    const= [0 for i in range(16)]
    with open('setpoints_Cryov2.txt','r+') as csvfile:
        reader = csv.reader(csvfile, delimiter=' ')
        i=0
        for row in reader:
            const[i] = row[2]
            const[i] = float(const[i])
            i+=1
        i-=1
        Channels = int(const[i])
    return Channels



def getSetpoints():

    #cur.execute("SELECT * FROM `wavemeter cryoqsim`.`setpoint`")
    cur.execute("SELECT * FROM `chipwavemeter`.`setpoint`")
    rows = cur.fetchall()
    if(len(rows) > 0): return rows[0]
    else: return None


    #Channels = getChannels()
    #setPoints= [0 for i in range(Channels)]
###### Commented by GP. Uncomment and comment lines below to do the online tracking
##    with open('setpoints_Cryo.csv','r+') as csvfile:
##        reader = csv.reader(csvfile, delimiter=' ')
##        i=0
##        for row in reader:
##            setPoints[i] = row[2]
##            setPoints[i] = float(setPoints[i])
##            i+=1
##            if i== Channels:
##                break
##    return setPoints

def getFreqs():
    Channels = getChannels()
    name = "WavemeterData.exe "
    name = name+str(8)
    with open(os.devnull, "w") as fnull:
        test = subprocess.call(name, stdout = fnull,shell=True) # Added shell True to avoid the shell to pop out, GP 11/15
    waveOut = str(subprocess.check_output( name,shell=True))     # Added shell True to avoid the shell to pop out, GP 11/15
    #print waveOut
    waveOut = waveOut.split(" ")
    #test = waveOut
    freq = [0,0,0]
    print (waveOut)
    freq[0] = float(waveOut[1]) # 399
    freq[1] = float(waveOut[2]) # 935
    freq[2] = float(waveOut[7]) # 369
    #freq[3] = float(waveOut[4])
    j=0

    #headers = {'content-type': 'application/json'}
    #url = "http://192.168.2.50/wavemeter/wavemeter/wavemeter-status"
    #dataSend = "5|0|5|http://192.168.2.50/wavemeter/wavemeter/|CAE770F80E4A681B200769F57E4D8989|edu.umd.ion.wavemeter.service.WavemeterService|pollWavemeter|edu.umd.ion.wavemeter.service.WavemeterDataMask/1786418976|1|2|3|4|1|5|5|0|1918500334|"
    #headers = {'Content-Type':'text/x-gwt-rpc; charset=utf-8','X-GWT-Permutation':'E1D57440910859B69F5FD923FD39B973','X-GWT-Module-Base':'http://192.168.2.50/wavemeter/wavemeter/'}
    #r = requests.post(url, data=dataSend, headers = headers)

    #result = re.match(r"\/\/OK\[(.+)\]", r.text)
    #wavelengths = result.groups()[0].split(',')
    # print wavelengths
    # print wavelengths[118]
    #freq[1] = float(wavelengths[306])
    #freq[2] = float(wavelengths[118])
    return freq

def getErrors():
    Channels = getChannels()
    freqError = [0 for i in range(Channels)]
    setPoints = getSetpoints()
    freqAct = getFreqs()
    j=0
    while True:
        freqError[j] = freqAct[j]-setPoints[j]
        j+=1
        if j == Channels:
            break
    return freqError


######  Commented by GP. To do the online tracking
#def Lock(con, cur):
######  Commented by GP. To do the online tracking

def Lock(con, cur):
    freq = getFreqs()
    setPoints = getSetpoints()
    # Offset in Volts
    offset_369 = 0
    offset_369b = 0
    offset_399 = 2.048 # This is the middle point of the output
    offset_935 = 0
    GlobalGain369 = 20
    GlobalGain369b = 1
    GlobalGain399 = 0.1
    GlobalGain935 = 30

    integr369 = 400
    integr369b = 400
    integr399 = 0
    integr935 = 500

    LaserLock_369 = PID(P=200, I=integr369, D=0)
    LaserLock_369b = PID(P=400, I=integr369b, D=0)
    LaserLock_399 = PID(P=3, I=integr399, D=0)
    LaserLock_935 = PID(P=350, I=integr935, D=0)

    LaserLock_369.setPoint(setPoints[0])
    LaserLock_369b.setPoint(setPoints[1])
    LaserLock_399.setPoint(setPoints[2])
    LaserLock_935.setPoint(setPoints[3])
    ADDA1.setVoltage(0, offset_399)
    # ADDA1.setVoltage(1, 0)
    # ADDA1.setVoltage(2, 0)

    print(offset_369,offset_369b,offset_399,offset_935)

    timeFlag_1 = False
    overTime = time.mktime(datetime.datetime.now().timetuple())

    errorCount=-1

    unlock_369 = 0
    unlock_369b = 0
    unlock_399 = 0
    unlock_935 = 0

    broke_369 = 0
    broke_369b = 0
    broke_399 = 0
    broke_935 = 0

    while True:
        freq = getFreqs()
        t = getSetpoints()
        if(t != None):
            setPoints = getSetpoints()
            if(LaserLock_369.set_point != setPoints[0]): LaserLock_369.setPoint(setPoints[0])
            if(LaserLock_369b.set_point != setPoints[1]): LaserLock_369b.setPoint(setPoints[1])
            if(LaserLock_399.set_point != setPoints[2]): LaserLock_399.setPoint(setPoints[2])
            if(LaserLock_935.set_point != setPoints[3]): LaserLock_935.setPoint(setPoints[3])

        for i in range(len(freq)):
            if freq[i]<0:
                freq[i] = setPoints[i]


        lock_369 = setPoints[4]
        lock_369b = setPoints[5]
        lock_399 = setPoints[6]
        lock_935 = setPoints[7]

        if (lock_369 == 1 and unlock_369 == 0):
            LaserLock_369.setKi(integr369)
            error_369 = LaserLock_369.update(freq[2])
        else:
            LaserLock_369.setKi(0)
            LaserLock_369.setIntegrator(0)
            error_369 = 0
            if (lock_369 == 0):
                unlock_369 = 0
                broke_369 = 0

        if (lock_369b == 1 and unlock_369b == 0):
            LaserLock_369b.setKi(integr369b)
            error_369b = LaserLock_369b.update(freq[0])
        else:
            LaserLock_369b.setKi(0)
            LaserLock_369b.setIntegrator(0)
            error_369b = 0
            if (lock_369b == 0):
                unlock_369b = 0
                broke_369b = 0

        if (lock_399 != 0 and unlock_399 == 0):
            LaserLock_399.setKi(integr399)
            error_399 = LaserLock_399.update(freq[0])
        else:
            LaserLock_399.setKi(0)
            LaserLock_399.setIntegrator(0)
            error_399 = 0
            if (lock_399 == 0):
                unlock_399 = 0
                broke_399 = 0

        if (lock_935 != 0 and unlock_935 == 0):
            LaserLock_935.setKi(integr935)
            error_935 = LaserLock_935.update(freq[1])
        else:
            LaserLock_935.setKi(0)
            LaserLock_935.setIntegrator(0)
            error_935 = 0
            if (lock_935 == 0):
                unlock_935 = 0
                broke_935 = 0

        print("freq = ", freq)
        print("Setpoints = ", setPoints)
        max_error = 5
        if (np.absolute(error_369)>=max_error):
            print("369 Lock Broken!")
            broke_369 = 1
            unlock_369 = 1
        if (np.absolute(error_369b)>=10*max_error):
            print("369b Lock Broken!")
            broke_369b = 1
            unlock_369b = 1
        if (np.absolute(error_399)>=max_error):
            print("399 Lock Broken!")
            broke_399 = 1
            unlock_399 = 1
        if (np.absolute(error_935)>=max_error):
            print("935 Lock Broken!")
            broke_935 = 1
            unlock_935 = 1

        dac369 = offset_369 + GlobalGain369 * error_369
        dac369b = offset_369b + GlobalGain369b * error_369b
        dac399 = offset_399 + GlobalGain399 * error_399
        dac935 = offset_935 + GlobalGain935 * error_935

        ADDA1.setVoltage(0, dac_399)
        # ADDA1.setVoltage(1, dac_399)
        # ADDA1.setVoltage(2, dac_935)

        cTime = time.mktime(datetime.datetime.now().timetuple())*1e3 + datetime.datetime.now().microsecond/1e3

        ###### To do the online tracking
        cur.execute("INSERT INTO `chipwavemeter`.`error` (time, `369`, `369b`, `399`, `935`, 369w, 369bw, 399w, 935w) VALUES (\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\');",(cTime,round(error_369,4), round(error_369b,4), round(error_399,4), round(error_935,4), freq[2], freq[0], freq[0], freq[1]))
        ##cur.execute("INSERT INTO `wavemeter`.`dac` (`369`, `369b`, `399`, `935`) VALUES (\'%s\',\'%s\',\'%s\',\'%s\');",(round(dac369,4), round(dac369b,4), round(dac399,4), round(dac935,4)))
        cur.execute("UPDATE `dac` SET `369`=\'%s\', `369b`=\'%s\', `399`=\'%s\', `935`=\'%s\' WHERE 1",(round(dac369,4), round(dac369b,4), round(dac399,4), round(dac935,4)))
        cur.execute("UPDATE `setpoint` SET `broke369`=\'%s\', `broke369b`=\'%s\', `broke399`=\'%s\', `broke935`=\'%s\' WHERE 1",(broke_369, broke_369b, broke_399, broke_935))
        con.commit()
        ###### To do the online tracking


##@atexit.register
##def reset_voltages():
##    print "killed!"
## ##    ADDA1.setVoltage(0,0)
## ##    ADDA1.setVoltage(3,0)
## ##    ADDA1.setVoltage(1,0)
## ##    ADDA1.setVoltage(2,0)
##    ADDA369.setVolt(offset_369)# GP: V=2.5 when it unlocks
##    ADDA369.stop()
##    ADDA369b.setVolt(offset_369b)# GP: V=2.5 when it unlocks
##    ADDA369b.stop()
##    ADDA399.setVolt(offset_399)# GP: V=2.5 when it unlocks
##    ADDA399.stop()
##    ADDA935.setVolt(offset_935)# GP: V=2.5 when it unlocks
##    ADDA935.stop()


ADDA1 = ADDA()

######To do the online tracking
#con = mdb.connect('127.0.0.1', 'python', 'cVvVc6wvZ4RQKMhn', 'wavemeter cryoqsim')
con = mdb.connect(host = '127.0.0.1', user = 'python',passwd = 'abc123',db = 'chipwavemeter',port = 3306, connect_timeout = 1000)
cur = con.cursor()
cur.execute("TRUNCATE TABLE `error`")
Lock(con, cur)
######To do the online tracking

