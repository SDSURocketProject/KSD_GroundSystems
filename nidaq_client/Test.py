import nidaqmx
import time
import nidaq_class

system = nidaqmx.system.System.local()
# # x = nidaqmx.system._collections.device_collection.DeviceCollection().__getitem__("DAQ-9189")
# x = nidaqmx.system.device.Device("DAQ-9189").reset_device()
# time.sleep(10)
for device in system.devices:
    if device.product_category == device.product_category.C_SERIES_MODULE:
        print('Device Name: {0}, Product Category: {1}, Product Type: {2}'.format(
            device.name, device.product_category, device.product_type))

for device in system.devices:
    if device.product_category == device.product_category.C_SERIES_MODULE:
        print('Device Name: {0}, Product Category: {1}, Product Type: {2}'.format(
            device.name, device.product_category, device.product_type))
