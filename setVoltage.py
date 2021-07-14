
# This is an interpretation of the example program
# C:\Program Files\National Instruments\NI-DAQ\Examples\DAQmx ANSI C\Analog Out\Generate Voltage\Cont Gen Volt Wfm-Int Clk\ContGen-IntClk.c
# This routine will play an arbitrary-length waveform file.
# This module depends on:
# numpy
# Adapted by Martin Bures [ mbures { @ } zoll { . } com ]

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
                    float64(self.curVolt),None))
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
    print("ion")
    mythread0 = SetVoltage( 0 , "Dev7/ao0")
    mythread1 = SetVoltage( 0 , "Dev7/ao1")
    mythread2 = SetVoltage( 0 , "Dev7/ao2")
    mythread3 = SetVoltage( 0 , "Dev7/ao3")
    mythread4 = SetVoltage( 0 , "Dev7/ao4")
    mythread5 = SetVoltage( 0 , "Dev7/ao5")
    mythread6 = SetVoltage( 0 , "Dev7/ao6")
    mythread7 = SetVoltage( 0 , "Dev7/ao7")
    mythread8 = SetVoltage( 0 , "Dev8/ao0")
    mythread9 = SetVoltage( 0 , "Dev8/ao1")
    mythread10 = SetVoltage( 0 , "Dev8/ao2")
    mythread11 = SetVoltage( 0 , "Dev8/ao3")
    mythread12 = SetVoltage( 0 , "Dev8/ao4")
    mythread13 = SetVoltage( 0 , "Dev8/ao5")
    mythread14 = SetVoltage( 0 , "Dev8/ao6")
    mythread15 = SetVoltage( 0 , "Dev8/ao7")
    mythread16 = SetVoltage( 0 , "Dev9/ao0")
    mythread17 = SetVoltage( 0 , "Dev9/ao1")
    mythread18 = SetVoltage( 0 , "Dev9/ao2")
    mythread19 = SetVoltage( 0 , "Dev9/ao3")
    mythread20 = SetVoltage( 0 , "Dev9/ao4")
    mythread21 = SetVoltage( 0 , "Dev9/ao5")
    mythread22 = SetVoltage( 0 , "Dev9/ao6")
    mythread23 = SetVoltage( 0 , "Dev9/ao7")

    mythread0.start()
    mythread1.start()
    mythread2.start()
    mythread3.start()
    mythread4.start()
    mythread5.start()
    mythread6.start()
    mythread7.start()
    mythread8.start()
    mythread9.start()
    mythread10.start()
    mythread11.start()
    mythread12.start()
    mythread13.start()
    mythread14.start()
    mythread15.start()
    mythread16.start()
    mythread17.start()
    mythread18.start()
    mythread19.start()
    mythread20.start()
    mythread21.start()
    mythread22.start()
    mythread23.start()

    print("Wait 2 s")
    time.sleep( 2 )
    print("Wait 10 s")
    mythread0.setVolt(0.5)
    mythread1.setVolt(1)
    mythread2.setVolt(1.5)
    mythread3.setVolt(2)
    mythread4.setVolt(2.5)
    mythread5.setVolt(3)
    mythread6.setVolt(3.5)
    mythread7.setVolt(4)
    mythread8.setVolt(4.5)
    mythread9.setVolt(5)
    mythread10.setVolt(5.5)
    mythread11.setVolt(6)
    mythread12.setVolt(6.5)
    mythread13.setVolt(0)
    mythread14.setVolt(0)
    mythread15.setVolt(0)
    mythread16.setVolt(0)
    mythread17.setVolt(0)
    mythread18.setVolt(0)
    mythread19.setVolt(0)
    mythread20.setVolt(0)
    mythread21.setVolt(0)
    mythread22.setVolt(0.0)
    mythread23.setVolt(0.0)

    time.sleep( 10 )
    print("Wait 1 s")
    time.sleep( 1 )

    mythread0.stop()
    mythread1.stop()
    mythread2.stop()
    mythread3.stop()
    mythread4.stop()
    mythread5.stop()
    mythread6.stop()
    mythread7.stop()
    mythread8.stop()
    mythread9.stop()
    mythread10.stop()
    mythread11.stop()
    mythread12.stop()
    mythread13.stop()
    mythread14.stop()
    mythread15.stop()
    mythread16.stop()
    mythread17.stop()
    mythread18.stop()
    mythread19.stop()
    mythread20.stop()
    mythread21.stop()
    mythread22.stop()
    mythread23.stop()
