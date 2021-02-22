import nidaqmx
import time

task1 = nidaqmx.system.storage.persisted_task.PersistedTask('brandttemptask').load()
while True:
    print(task1.read())
task1.close()

#task = nidaqmx.Task()
#task.ai_channels.add_ai_thrmcpl_chan("NI9213-Mod5/ai0")
# task1 = nidaqmx.system.storage.persisted_task.PersistedTask("MyTemperatureTask_0").load()

#while True:
#    print(task.read(number_of_samples_per_channel=50))
    