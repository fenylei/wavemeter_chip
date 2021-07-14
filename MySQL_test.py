import MySQLdb as mdb
import sys
import random
import time, datetime
import math
import csv
import os
import subprocess
#con = mdb.connect('127.0.0.1', 'python','abc123','test')

#cur = con.cursor()

# Please construct a table first working or else the below code won't work  WL

#sql = "INSERT INTO customer (name, address) VALUES (%s, %s)"
#val = ("John", "Highway 21")
#cur.execute(sql, val)
#con.commit()

#con = mdb.connect('127.0.0.1', 'python','abc123','wavemeter')
#cur = con.cursor()
#sql = "INSERT INTO setpoint (setpt1,setpt2,setpt3,setpt4,lock369,lock369b,lock399,lock935,broke369,broke369b,broke399,broke935) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
#val = (811.292330,811.292330,751.527230,320.57173,0,0,0,0,1,1,1,1)
#sql = "INSERT INTO trying (setpt,error,broke) VALUES (%s,%s,%s)"
#val = (811.292330,0,1)
#cur.execute(sql, val)
#con.commit()

#cur.execute("INSERT INTO `wavemeter cryoqsim`.`error` (time, `369`, `369b`, `399`, `935`, 369w, 369bw, 399w, 935w) VALUES (\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\');", \
#        (cTime, round(error_369, 4), round(error_369b, 4), round(error_399, 4), round(error_935, 4), freq[0], freq[3], freq[1], freq[2]))
#cur.execute("UPDATE `setpoint` SET `broke369`=\'%s\', `broke369b`=\'%s\', `broke399`=\'%s\', `broke935`=\'%s\' WHERE 1",(broke_369, broke_369b, broke_399, broke_935))




Channels = 4
name = "WavemeterData.exe "
name = name+str(7)
with open(os.devnull, "w") as fnull:
    test = subprocess.call(name, stdout = fnull,shell=True) # Added shell True to avoid the shell to pop out, GP 11/15
waveOut = str(subprocess.check_output(name, shell=True))
#     print subprocess.check_output(name, shell=True)
#print(test)
#    # Added shell True to avoid the shell to pop out, GP 11/15
print waveOut
waveOut = waveOut.split(" ")
# #test = waveOut
freq = [0,0,0,0]
# print (waveOut)
freq[0] = float(waveOut[0])
freq[1] = float(waveOut[1])
freq[2] = float(waveOut[2])
freq[3] = float(waveOut[5])

print freq


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

print Channels
print const