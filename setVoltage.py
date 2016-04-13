"""
This is an interpretation of the example program
C:\Program Files\National Instruments\NI-DAQ\Examples\DAQmx ANSI C\Analog Out\Generate Voltage\Cont Gen Volt Wfm-Int Clk\ContGen-IntClk.c
This routine will play an arbitrary-length waveform file.
This module depends on:
numpy
Adapted by Martin Bures [ mbures { @ } zoll { . } com ]
"""
# import system libraries
import ctypes
import numpy
import threading
# load any DLLs
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
##############################
minvolt=-10
maxvolt=10

class SetVoltage( threading.Thread ):
    """
    This class performs the necessary initialization of the DAQ hardware and
    spawns a thread to handle playback of the signal.
    It takes as input arguments the waveform to play and the sample rate at which
    to play it.
    This will play an arbitrary-length waveform file.
    """
    def __init__( self, initVolt, aoName ):
        self.running = True
        self.taskHandle = TaskHandle( 0 )
        self.curVolt = initVolt
        self.aoName = aoName
        # setup the DAQ hardware
        self.CHK(nidaq.DAQmxCreateTask("",
                          ctypes.byref( self.taskHandle )))
        self.CHK(nidaq.DAQmxCreateAOVoltageChan( self.taskHandle,
                                   self.aoName,
                                   "",
                                   float64(minvolt),
                                   float64(maxvolt),
                                   DAQmx_Val_Volts,
                                   None))
        self.CHK(nidaq.DAQmxWriteAnalogScalarF64( self.taskHandle,
                              1,
                              float64(-1),
                              float64(self.curVolt),
                              None))
        threading.Thread.__init__( self )
    def CHK( self, err ):
        """a simple error checking routine"""
        if err < 0:
            buf_size = 300
            buf = ctypes.create_string_buffer('\000' * buf_size)
            nidaq.DAQmxGetErrorString(err,ctypes.byref(buf),buf_size)
            raise RuntimeError('nidaq call failed with error %d: %s'%(err,repr(buf.value)))
        if err > 0:
            buf_size = 300
            buf = ctypes.create_string_buffer('\000' * buf_size)
            nidaq.DAQmxGetErrorString(err,ctypes.byref(buf),buf_size)
            raise RuntimeError('nidaq generated warning %d: %s'%(err,repr(buf.value)))
    def run( self ):
        counter = 0
        self.CHK(nidaq.DAQmxStartTask( self.taskHandle ))
##    def setVolt ( self, voltage ):
##        self.curVolt = voltage;
##        self.CHK(nidaq.DAQmxWriteAnalogScalarF64(self.taskHandle,
##                      1,
##                      float64(-1),
##                      float64(self.curVolt),
##                      None))
    def setVolt ( self, voltage ):
        self.curVolt = voltage;
        if voltage>maxvolt:
            print("WARNING: voltage too high on", self.aoName)
            self.curVolt=maxvolt
        if voltage<minvolt:
            print("WARNING: voltage too low on ", self.aoName)
            self.curVolt=minvolt
        self.CHK(nidaq.DAQmxWriteAnalogScalarF64(self.taskHandle,
                    1,
                    float64(-1),
                    float64(self.curVolt),
                    None))
        # print("volt = ",self.curVolt)
    def stop( self ):
        self.running = False
        nidaq.DAQmxStopTask( self.taskHandle )
        nidaq.DAQmxClearTask( self.taskHandle )

class SetVoltage6009( threading.Thread ):
    """
    This class performs the necessary initialization of the DAQ hardware and
    spawns a thread to handle playback of the signal.
    It takes as input arguments the waveform to play and the sample rate at which
    to play it.
    This will play an arbitrary-length waveform file.
    """
    def __init__( self, initVolt, aoName ):
        self.running = True
        self.taskHandle = TaskHandle( 0 )
        self.curVolt = initVolt
        self.aoName = aoName
        # setup the DAQ hardware
        self.CHK(nidaq.DAQmxCreateTask("",
                          ctypes.byref( self.taskHandle )))
        self.CHK(nidaq.DAQmxCreateAOVoltageChan( self.taskHandle,
                                   self.aoName,
                                   "",
                                   float64(0),
                                   float64(5),
                                   DAQmx_Val_Volts,
                                   None))
        self.CHK(nidaq.DAQmxWriteAnalogScalarF64( self.taskHandle,
                              1,
                              float64(-1),
                              float64(self.curVolt),
                              None))
        threading.Thread.__init__( self )
    def CHK( self, err ):
        """a simple error checking routine"""
        if err < 0:
            buf_size = 200
            buf = ctypes.create_string_buffer('\000' * buf_size)
            nidaq.DAQmxGetErrorString(err,ctypes.byref(buf),buf_size)
            raise RuntimeError('nidaq call failed with error %d: %s'%(err,repr(buf.value)))
        if err > 0:
            buf_size = 200
            buf = ctypes.create_string_buffer('\000' * buf_size)
            nidaq.DAQmxGetErrorString(err,ctypes.byref(buf),buf_size)
            raise RuntimeError('nidaq generated warning %d: %s'%(err,repr(buf.value)))
    def run( self ):
        counter = 0
        self.CHK(nidaq.DAQmxStartTask( self.taskHandle ))
##    def setVolt ( self, voltage ):
##        self.curVolt = voltage;
##        self.CHK(nidaq.DAQmxWriteAnalogScalarF64(self.taskHandle,
##                      1,
##                      float64(-1),
##                      float64(self.curVolt),
##                      None))
    def setVolt ( self, voltage ):
        self.curVolt = voltage;
        if voltage>5:
            print("WARNING: NI6009 voltage too high")
            self.curVolt=5
        if voltage<0:
            print("WARNING: NI6009 voltage too low")
            self.curVolt=0
        self.CHK(nidaq.DAQmxWriteAnalogScalarF64(self.taskHandle,
                    1,
                    float64(-1),
                    float64(self.curVolt),
                    None))
        # print("volt = ",self.curVolt)
    def stop( self ):
        self.running = False
        nidaq.DAQmxStopTask( self.taskHandle )
        nidaq.DAQmxClearTask( self.taskHandle )



if __name__ == '__main__':
    import time
    mythread0 = SetVoltage( 0 , "PXI1Slot2/ao0")
    mythread1 = SetVoltage( 0 , "PXI1Slot2/ao1")
    mythread2 = SetVoltage6009( 2.5 , "Dev1/ao0")

    mythread0.start()
    mythread1.start()
    mythread2.start()
    print("2.5 V + 2 s")
    time.sleep( 2 )
    print("5 V + 5 s")
    mythread0.setVolt(10)
    mythread1.setVolt(10)
    mythread2.setVolt(2)
    time.sleep( 5 )
    print("0 V + 2 s")
    mythread0.setVolt(-10)
    mythread1.setVolt(-10)
    mythread2.setVolt(0)
    time.sleep( 2 )
    print("2.5 V")
    mythread0.setVolt(0)
    mythread1.setVolt(0)
    mythread2.setVolt(2.5)

    mythread0.stop()
    mythread1.stop()
    mythread2.stop()
