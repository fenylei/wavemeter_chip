import subprocess
import csv
import time, datetime
import MySQLdb as mdb
#import pymysql
from PID import PID
# from ADDA import ADDA  # DAC interface by Chip lab. We should do our own.
#import setVoltage
import winsound
import atexit
import numpy as np
import requests
import re
import os
import time
#import wx



def getChannels():
    const= [0 for i in range(16)]
    with open('setpoints_Cryo.csv','r+') as csvfile:
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


    cur.execute("SELECT * FROM `wavemeter`.`setpoint`")
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
    name = name+str(7)
    with open(os.devnull, "w") as fnull:
        test = subprocess.call(name, stdout = fnull,shell=True) # Added shell True to avoid the shell to pop out, GP 11/15
    waveOut = str(subprocess.check_output(name,shell=True))     # Added shell True to avoid the shell to pop out, GP 11/15
    waveOut = waveOut.split(" ")
    test = waveOut
    freq = [0,0,0, 0]
##    print waveOut
    freq[0] = float(waveOut[6])
    freq[1] = float(waveOut[0])
    freq[2] = float(waveOut[5])
    freq[3] = float(waveOut[4])
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
    setPoints = getSetpoints()
    offset_369=0 # Offset in Volts
    offset_399=0
    offset_935=0
    GlobalGain369=20
    GlobalGain399=18
    GlobalGain935=30

    integr369 = 400
    integr399 = 300
    integr935 = 500

    LaserLock_369 = PID(P=200, I=integr369, D=0)
    LaserLock_399 = PID(P=300, I=integr399, D=0)
    LaserLock_935 = PID(P=350, I=integr935, D=0)

    LaserLock_369.setPoint(setPoints[0])
    LaserLock_399.setPoint(setPoints[1])
    LaserLock_935.setPoint(setPoints[2])

    #ADDA1.setVoltage(0,0)
    #ADDA1.setVoltage(1,0)
    #ADDA1.setVoltage(2,0)
    #ADDA369=setVoltage.SetVoltage(offset_369, "PXI1Slot4/ao4")# to define a single thread outside the while cycle
    #ADDA369.setVolt(offset_369)
    #ADDA399=setVoltage.SetVoltage(offset_399, "PXI1Slot4/ao5")# to define a single thread outside the while cycle
    #ADDA399.setVolt(offset_399)
    #ADDA935=setVoltage.SetVoltage(offset_935, "PXI1Slot4/ao6")# to define a single thread outside the while cycle
    #ADDA935.setVolt(offset_935)

    print(offset_369,offset_399,offset_935)

    timeFlag_1 = False
    overTime = time.mktime(datetime.datetime.now().timetuple())

    errorCount=-1
    while True:
        freq = getFreqs()
        t = getSetpoints()
        if(t != None):
            setPoints = getSetpoints()
            if(LaserLock_369.set_point != setPoints[0]): LaserLock_369.setPoint(setPoints[0])
            if(LaserLock_399.set_point != setPoints[1]): LaserLock_399.setPoint(setPoints[1])
            if(LaserLock_935.set_point != setPoints[2]): LaserLock_935.setPoint(setPoints[2])

        for i in range(len(freq)):
            if freq[i]<0:
                freq[i] = setPoints[i]


        lock_369 = setPoints[3]
        lock_399 = setPoints[4]
        lock_935 = setPoints[5]

        if (lock_369 != 0):
            LaserLock_369.setKi(integr369)
            error_369 = LaserLock_369.update(freq[0])
            #print ("error 369 = ",error_369)
        else:
            LaserLock_369.setKi(0)
            LaserLock_369.setIntegrator(0)
            error_369 = 0

        if (lock_399 != 0):
            LaserLock_399.setKi(integr399)
            error_399 = LaserLock_399.update(freq[1])
            #print ("error 399 = ",error_399)
        else:
            LaserLock_399.setKi(0)
            LaserLock_399.setIntegrator(0)
            error_399 = 0

        if (lock_935 != 0):
            LaserLock_935.setKi(integr935)
            error_935 = LaserLock_935.update(freq[2])
            #print ("error 935 = ",error_935)
        else:
            LaserLock_935.setKi(0)
            LaserLock_935.setIntegrator(0)
            error_935 = 0

        print("freq = ", freq)
        print("Setpoints = ", setPoints)
        max_error = 5
        if (np.absolute(error_369)>=max_error):
            print("369 Lock Broken!")
            broke_369 = 1
            #ADDA369.setVolt(offset_369)# GP: V=0 when it unlocks
            #ADDA369.stop()
        else:
            broke_369 = 0
        if (np.absolute(error_399)>=max_error):
            print("399 Lock Broken!")
            broke_399 = 1
            #ADDA399.setVolt(offset_399)# GP: V=0 when it unlocks
            #ADDA399.stop()
        else:
            broke_399 = 0
        if (np.absolute(error_935)>=max_error):
            print("935 Lock Broken!")
            broke_935 = 1
            #ADDA935.setVolt(offset_935)# GP: V=0 when it unlocks
            #ADDA935.stop()
        else:
            broke_935 = 0
        #ADDA369.setVolt(offset_369 + GlobalGain369*error_369)
        #ADDA399.setVolt(offset_399 + GlobalGain399*error_399)
        #ADDA935.setVolt(offset_935 + GlobalGain935*error_935)
        cTime = time.mktime(datetime.datetime.now().timetuple())*1e3 + datetime.datetime.now().microsecond/1e3

        ###### To do the online tracking
        cur.execute("INSERT INTO `wavemeter`.`error` (time, `369`, `399`, `935`, 369w, 399w, 935w) VALUES (\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\');",(cTime,round(error_369,4), round(error_399,4), round(error_935,4), freq[0], freq[1], freq[2]))
        cur.execute("UPDATE `setpoint` SET `broke369`=\'%s\', `broke399`=\'%s\', `broke935`=\'%s\' WHERE 1",(broke_369, broke_399, broke_935))
        con.commit()
        ###### To do the online tracking


##@atexit.register
##def reset_voltages():
##    print "killed!"
## ##    ADDA1.setVoltage(0,0)
## ##    ADDA1.setVoltage(1,0)
## ##    ADDA1.setVoltage(2,0)
##    ADDA369.setVolt(offset_369)# GP: V=2.5 when it unlocks
##    ADDA369.stop()
##    ADDA399.setVolt(offset_399)# GP: V=2.5 when it unlocks
##    ADDA399.stop()
##    ADDA935.setVolt(offset_935)# GP: V=2.5 when it unlocks
##    ADDA935.stop()


# ADDA1 = ADDA() # commented GP. Use new interface.

######To do the online tracking
#con = mdb.connect('127.0.0.1', 'python', 'cVvVc6wvZ4RQKMhn', 'wavemeter')
con = mdb.connect('127.0.0.1', 'python','abc123','wavemeter')
cur = con.cursor()
cur.execute("TRUNCATE TABLE `error`")
Lock(con, cur)
######To do the online tracking

