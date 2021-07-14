from setVoltage import SetVoltage

outputVolt_1 = SetVoltage(2.5, "Dev1/ao1")
outputVolt_2 = SetVoltage(2.5, "Dev1/ao0")
outputVolt_1.stop()
outputVolt_2.stop()

