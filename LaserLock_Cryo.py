import subprocess
import csv
import time, datetime
import MySQLdb as mdb
from PID import PID
# from ADDA import ADDA  # DAC interface by Chip lab. We should do our own.
#from setVoltage import SetVoltage
import setVoltage
import winsound
import atexit
import numpy as np
import requests
import re
import os
import time
#import wx


##global NI6009AO1
##global offset_369
##offset_369=2.5


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

    ###### Commented by GP. Uncomment and comment lines below to do the online tracking
##    cur.execute("SELECT * FROM `wavemeter`.`setpoint`")
##    rows = cur.fetchall()
##    if(len(rows) > 0): return rows[0]
##    else: return None
    ###### Commented by GP. Uncomment and comment lines below to do the online tracking

    Channels = getChannels()
    setPoints= [0 for i in range(Channels)]
    with open('setpoints_Cryo.csv','r+') as csvfile:
        reader = csv.reader(csvfile, delimiter=' ')
        i=0
        for row in reader:
            setPoints[i] = row[2]
            setPoints[i] = float(setPoints[i])
            i+=1
            if i== Channels:
                break
    return setPoints

def getFreqs():
    Channels = getChannels()
    name = "WavemeterData.exe "
    name = name+str(3)
    with open(os.devnull, "w") as fnull:
        test = subprocess.call(name, stdout = fnull,shell=True) # Added shell True to avoid the shell to pop out, GP 11/15
    waveOut = str(subprocess.check_output(name,shell=True))     # Added shell True to avoid the shell to pop out, GP 11/15
    waveOut = waveOut.split(" ")
    test = waveOut
    freq = [0,0,0]
##    print waveOut
    freq[0] = float(waveOut[0])
    freq[1] = float(waveOut[1])
    freq[2] = float(waveOut[2])
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

def Lock():
    setPoints = getSetpoints()
    offset_369=2.5 # Offset in Volts
    offset_399=2.5
    offset_935=2.5
    GlobalGain369=20
    GlobalGain399=20
    GlobalGain935=30

    LaserLock_369 = PID(P=100, I=300, D=0)
    LaserLock_399 = PID(P=300, I=500, D=0)
    LaserLock_935 = PID(P=2, I=2, D=0)

    LaserLock_369.setPoint(setPoints[0])
    LaserLock_399.setPoint(setPoints[1])
    LaserLock_935.setPoint(setPoints[2])

    #ADDA1.setVoltage(0,0)
    #ADDA1.setVoltage(1,0)
    #ADDA1.setVoltage(2,0)# new interface needed
    offset_369=2.5 # Offset in Volts
    offset_399=2.5
    offset_935=2.5
    ADDA369=setVoltage.SetVoltage(offset_369, "PXI1Slot2/ao0")# to define a single thread outside the while cycle
    ADDA369.setVolt(offset_369)
    ADDA399=setVoltage.SetVoltage(offset_399, "PXI1Slot2/ao1")# to define a single thread outside the while cycle
    ADDA399.setVolt(offset_399)
    ADDA935=setVoltage.SetVoltage(offset_935, "Dev1/ao0")# to define a single thread outside the while cycle
    ADDA935.setVolt(offset_935)

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

            #freq[0] = setPoints[0]
        error_369 = LaserLock_369.update(freq[0])
        error_399 = LaserLock_399.update(freq[1])*0
        error_935 = LaserLock_935.update(freq[2])*0

        print("freq = ", freq)
        print("Setpoints = ", setPoints)
        # print round(error_369,4), round(error_399,4), round(error_935,4)
        #time.sleep(.3)
##        if (error_369**2>=25) or(error_399**2>=25) or(error_935**2>=25):#11/15 GP
        if (np.absolute(error_369)>=1) or (np.absolute(error_399)>=1) or (np.absolute(error_935)>=1):
            #winsound.PlaySound("SystemQuestion", winsound.SND_ALIAS)
            #winsound.PlaySound("SystemQuestion", winsound.SND_ALIAS)
            #winsound.PlaySound("SystemQuestion", winsound.SND_ALIAS)
            #winsound.PlaySound("SystemQuestion", winsound.SND_ALIAS)
##            ADDA1.setVoltage(0,0)
##            ADDA1.setVoltage(1,0)
##            ADDA1.setVoltage(2,0)
            ADDA369.setVolt(offset_369)# GP: V=2.5 when it unlocks
            ADDA369.stop()
            ADDA399.setVolt(offset_399)# GP: V=2.5 when it unlocks
            ADDA399.stop()
            ADDA935.setVolt(offset_935)# GP: V=2.5 when it unlocks
            ADDA935.stop()

            print "Lock Broken!"
            print (error_369, error_399, error_935)
            print("error too big = ", error_369)
            break
##        print("error is ", round(error_369,6))#, round(error_399,4), round(error_935,4)
##        ADDA1.setVoltage(0, error_369)
##        ADDA1.setVoltage(1, error_399)
##        ADDA1.setVoltage(2, error_935)
##        print(" V = ",offset_369 + GlobalGain369*error_369)
        ADDA369.setVolt(offset_369 + GlobalGain369*error_369)
        ADDA399.setVolt(offset_399 + GlobalGain399*error_399)
        ADDA935.setVolt(offset_935 + GlobalGain935*error_935)
##        print("=========================================")

        cTime = time.mktime(datetime.datetime.now().timetuple())*1e3 + datetime.datetime.now().microsecond/1e3

        #cur.execute("INSERT INTO `wavemeter`.`error`( `index`, `time`, `739`, `935`, `739w`, `935w`) VALUES (NULL, \'%s\',\'%s\',\'%s\',\'%s\',\'%s\');",(cTime,error_2,error_1, freq[1], freq[0]))
        #con.commit()

        ###### Commented by GP. To do the online tracking
        #cur.execute("INSERT INTO `wavemeter`.`error` (time, `369`, `399`, `935`, 369w, 399w, 935w) VALUES (\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\');",(cTime,0, round(error_399,4), round(error_935,4), freq[0], freq[1], freq[2]))
        #con.commit()
        ###### Commented by GP. To do the online tracking

        # break

@atexit.register
def reset_voltages():
    print "killed!"
##    ADDA1.setVoltage(0,0)
##    ADDA1.setVoltage(1,0)
##    ADDA1.setVoltage(2,0)
    ADDA369.setVolt(offset_369)# GP: V=2.5 when it unlocks
    ADDA369.stop()
    ADDA399.setVolt(offset_399)# GP: V=2.5 when it unlocks
    ADDA399.stop()
    ADDA935.setVolt(offset_935)# GP: V=2.5 when it unlocks
    ADDA935.stop()


######Commented by GP. To do the online tracking
#con = mdb.connect('192.168.9.2', 'python', 'dTh6xh', 'wavemeter')
#cur = con.cursor()
#cur.execute("TRUNCATE TABLE `error`")
#Lock(con, cur)
######Commented by GP. To do the online tracking

Lock()
#some change
#another change
