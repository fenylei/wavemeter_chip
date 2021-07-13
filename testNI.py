import ctypes
import numpy as np
from string import *
##from nidaqmx import AnalogOutputTask

nidaq = ctypes.windll.nicaiu # load the DLL

##############################
# Setup some typedefs and constants
# to correspond with values in
# C:\Program Files\National Instruments\NI-DAQ\DAQmx ANSI C Dev\include\NIDAQmx.h

# the typedefs
int32 = ctypes.c_long
uInt32 = ctypes.c_ulong
uInt64 = ctypes.c_ulonglong
float64 = ctypes.c_double
TaskHandle = uInt32
# the constants
DAQmx_Val_Cfg_Default = int32(-1)
DAQmx_Val_Volts = 10348
DAQmx_Val_Rising = 10280
DAQmx_Val_FiniteSamps = 10178
DAQmx_Val_ContSamps = 10123
DAQmx_Val_GroupByChannel = 0


buf_size = 30
buf = ctypes.create_string_buffer('\000' * buf_size)
#nidaq.DAQmxGetErrorString(err,ctypes.byref(buf),buf_size)

#nidaq.DAQmxGetSysDevNames(char *data, uInt32 bufferSize);
nidaq.DAQmxGetSysDevNames(buf, buf_size);
#print(ctypes.sizeof(buf), repr(buf.raw))
print(buf.raw)


 

##data = 9.95*np.sin(np.arange(1000, dtype=np.float64)*2*np.pi/1000)
##task = AnalogOutputTask()
##task.create_voltage_channel('Dev1/ao2', min_val=-10.0, max_val=10.0)
##task.configure_timing_sample_clock(rate = 1000.0)
##task.write(data)
##task.start()
##raw_input('Generating voltage continuously. Press Enter to interrupt..')
##task.stop()
##del task
