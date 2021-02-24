import nidaqmx
import csv
from datetime import datetime,date
import os
import time

class nidaqtask():
    def __init__(self, device, module, channel, sample_rate):
        self.sample_rate = sample_rate
        self.device = device
        self.module = module
        self.channel = channel
        self.task = nidaqmx.Task()

        if device.type == "9213":
            thermclp_setup(list_channels)

    def thermclp_setup(self, channels):
        for chan in channels:
            task.ai_channels.add_ai_thrmcpl_chan()
            self.task.ai_channels.add_ai_thrmcpl_chan("{}-{}/{}".format(self.device, self.module, self.channel))
            self.task.timing.cfg_samp_clk_timing(self.sample_rate,sample_mode=ni.constants.AcquisitionType.CONTINUOUS,samps_per_chan= 1)

    def start(self):
        run()
    
    def stop(self):
        self.task.close()

    def run(self):
        while stopper:


if __name__ == '__main__':
    x = nidaqtask(module_name, channel_list, sample_rate)
    x.start()
    time.sleep(10)
    x.stop()



