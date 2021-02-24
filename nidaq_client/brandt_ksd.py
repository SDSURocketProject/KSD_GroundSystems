import nidaqmx
import csv
from datetime import datetime,date
import os

Mod1 = ["ai0", "ai3"]
Mod2 = []
Mod3 = []
Mod4 = ["ai5", "ai6"]
Mod5 = []
Mod6 = []

task1 = nidaqmx.system.storage.persisted_task.PersistedTask('brandttemptask').load()
today = datetime.now()
date = today.strftime("%Y-%m-%d")
iteration = 1

while os.path.exists('nidaq_client/Logs/{}_thrmcpllog_{}.csv'.format(date,iteration)):
    iteration += 1

with open('nidaq_client/Logs/{}_thrmcpllog_{}.csv'.format(date,iteration),'w',newline='') as write_file:
    while True:
        csv_writer = csv.writer(write_file, delimiter= ',')
        csv_writer.writerow([datetime.now().strftime("%H:%M:%S.%f")[:-3],"%.03f" % task1.read()])

write_file.close()
task1.close()