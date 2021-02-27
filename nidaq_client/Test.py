import nidaqmx

system = nidaqmx.system.System.local()

for device in system.devices:
    print('Device Name: {0}, Product Category: {1}, Product Type: {2}'.format(
        device.name, device.product_category, device.product_type))