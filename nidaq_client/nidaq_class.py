import nidaqmx
import csv
from datetime import datetime,date
import os
import time
import set_timing_mode
from threading import Thread

class nidaqtask(Thread):
    def __init__(self, chassis, module, channels, sample_rate, sample_per_channel):
        self.sample_rate = sample_rate
        self.sample_per_channel = sample_per_channel
        self.module = module
        self.channels = channels
        self.chassis = chassis
        self.task = nidaqmx.Task()
        self.system = nidaqmx.system.System.local()
        self.setup()
        # nidaqmx.system.device.Device(self.chassis).reset_device()  #Need a time.sleep afterwards to initialize the modules
        # time.sleep(10)

    def setup(self):
        for device in self.system.devices:
            if device.name == self.chassis + self.module:
                print(device.product_type)
                if "9213" in device.product_type:
                    self.thermcpl_setup(self.channels)
                elif "9485" in device.product_type:
                    print("Do voltage output stuff")
                elif "9205" in device.product_type:
                    self.voltage_setup(self.channels)
                elif "9237" in device.product_type:
                    print("Do output voltage/input voltage stuff")
                elif "9401" in device.product_type:
                    print("Do Digital input/output stuff")

    def thermcpl_setup(self, channels):
        for chan in channels:
            self.task.ai_channels.add_ai_thrmcpl_chan("{}{}/{}".format(self.chassis, self.module, chan))
            #set_timing_mode.cfg_samp_clk_timing(self.task._handle, nidaqmx.constants.ADCTimingMode.HIGH_SPEED)
            self.task.timing.adc_sample_high_speed()
            self.task.timing.cfg_samp_clk_timing(self.sample_rate,sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS,
                            samps_per_chan= self.sample_per_channel)
    
    def voltage_setup(self, channels):
        for chan in channels:
            self.task.ai_channels.add_ai_voltage_chan("{}{}/{}".format(self.chassis, self.module, chan))
            self.task.timing.cfg_samp_clk_timing(self.sample_rate,sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS,
                            samps_per_chan= self.sample_per_channel)
            self.task.timing.cfg

    def start(self):
        self.run()

    def stop(self):
        self.task.close()

    def run(self):
        while True:
            print(self.task.read())

if __name__ == '__main__':
    channels = ["ai0"]
    x = nidaqtask("DAQ-9189", "Mod5", channels, 60, 1)
    # y = nidaqtask("DAQ-9189", "Mod2", channels, 1000, 1)
    x.start()
    # y.start()
    x.stop()
    # y.stop()