import ok
import sys
import string
import time
import struct

class ADDA:
	def __init__(self):
		voltages = [0,0,0,0]

		self.xem = ok.okCFrontPanel()
		if (self.xem.NoError != self.xem.OpenBySerial("")):
			print ("A device could not be opened.  Is one connected?")
			#return(False)

		devInfo = ok.okTDeviceInfo()
		if (self.xem.NoError != self.xem.GetDeviceInfo(devInfo)):
			print ("Unable to retrieve device information.")
			exit
		print("Got device: " + devInfo.productName)

		if (self.xem.NoError != self.xem.ConfigureFPGA("dac.bit")):
			print ("FPGA configuration failed.")
			exit

	def setVoltage(self, channel, voltage):
		voltint = int(voltage / 4.096 * 0x10000)
		if voltint < 0:
			voltint = 0
		elif voltint > 0xffff:
			voltint = 0xffff
		data = int(channel) << 16 | voltint # low 16 bits is the value to be set, high 8 bit is channel number
		self.xem.SetWireInValue(0x00, data)
		self.xem.UpdateWireIns()
		self.xem.ActivateTriggerIn(0x40, 0)

ADDA1 = ADDA()
# ADDA1.setVoltage(0, 0.0)
# ADDA1.setVoltage(1, 0.00538)
# ADDA1.setVoltage(2, 1.0)
# ADDA1.setVoltage(3, -1.5)


