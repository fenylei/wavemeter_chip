import setVoltage
import time
import MySQLdb as mdb

offset_369 = 0  # Offset in Volts
offset_369b = 0
offset_399 = 0
offset_935 = 0

ADDA369=setVoltage.SetVoltage(offset_369, "Dev13/ao0")# to define a single thread outside the while cycle
ADDA369.setVolt(offset_369)
ADDA369b=setVoltage.SetVoltage(offset_369b, "Dev13/ao3")# to define a single thread outside the while cycle
ADDA369.setVolt(offset_369b)
ADDA399=setVoltage.SetVoltage(offset_399, "Dev13/ao1")# to define a single thread outside the while cycle
ADDA399.setVolt(offset_399)
ADDA935=setVoltage.SetVoltage(offset_935, "Dev13/ao6")# to define a single thread outside the while cycle
ADDA935.setVolt(offset_935)

var369 = 0
var369b = 0
var399 = 0
var935 = 0

def main(con, cur):

    while True:

        cur.execute("SELECT * FROM `wavemeter cryoqsim`.`dac`")
        rows = cur.fetchall()
        con.commit()
        if(len(rows) > 0): voltages = rows[0]
        var369=voltages[0]
        var369b=voltages[1]
        var399=voltages[2]
        var935=voltages[3]

        print(var369,var369b,var399,var935)

        ADDA369.setVolt(var369)
        ADDA369b.setVolt(var369b)
        ADDA399.setVolt(var399)
        ADDA935.setVolt(var935)

        time.sleep(.01)
        con.commit()

con = mdb.connect('129.2.116.80', 'cryolab', 'PPc9H9przGA5UFM6', 'wavemeter cryoqsim') ## Changed IP fron 129.2.116.28 to 129.2.116.80
cur = con.cursor()
main(con, cur)