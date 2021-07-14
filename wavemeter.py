#!/usr/bin/python

import MySQLdb as mdb
import sys
import random
import time, datetime
import math

##con = mdb.connect('127.0.0.1', 'data', 'data', 'test')
con = mdb.connect('127.0.0.1', 'python','abc123','wavemeter')

ii=0
with con:
    cur = con.cursor()
    while ii<10:
        rd369 = round(random.gauss(369.5, 0.2),7)+math.sin(0.2*time.clock())
        rd935 = round(random.gauss(935.5, 0.2),7)+math.sin(0.2*time.clock()+1)
        rd399 = round(random.gauss(399.5, 0.2),7)+math.sin(0.2*time.clock()+2)
        cTime = time.mktime(datetime.datetime.now().timetuple())*1e3 + datetime.datetime.now().microsecond/1e3
        #cur.execute("INSERT INTO `test`.`wavemeter` (`index`, `time`, `739`, `935`, `399`) VALUES (NULL, CURRENT_TIMESTAMP, \'739.0508561\', \'935.6142768\', \'399.33334\');")
        #cur.execute("INSERT INTO `wavemeter`.`test` (`index`, `time`, `369`, `935`, `399`) VALUES (NULL, \'%s\', \'%s\' , \'%s\' , \'%s\');",(cTime,rd369,rd935,rd399))
        cur.execute("INSERT INTO `wavemeter`.`trying` (`setpt`) VALUES (\'%s\');",(rd399))
        print(rd399)
        time.sleep(.02)
        con.commit()
        print ii
        ii=ii+1
