import nidaqmx
import csv
from datetime import datetime,date
import os

class nidaqtask():
    def __init__(self, sample_rate, device, module, channel):
        self.sample_rate = sample_rate
        self.device = device
        self.module = module
        self.channel = channel
        self.task = nidaqmx.Task()

    def thrmcpl(self):
        task.ai_channels.add_ai_thrmcpl_chan("{}-{}/{}".format(self.device, self.module, self.channel))
        task.timing.cfg_samp_clk_timing(self.sample_rate,sample_mode=ni.constants.AcquisitionType.CONTINUOUS,samps_per_chan= 1)

    def voltage(self):
        task.ai_channels.add_ai_voltage_chan("{}-{}/{}".format(self.device, self.module, self.channel))
        task.timing.cfg_samp_clk_timing(self.sample_rate,sample_mode=ni.constants.AcquisitionType.CONTINUOUS,samps_per_chan= 1)

task1.close()