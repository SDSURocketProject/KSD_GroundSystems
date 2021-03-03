#put the following function in task.timing library at end
def adc_sample_high_speed(
        self, channel="", sample_mode=14712):
    """
    Turn that shit up boi
    """
    cfunc = lib_importer.windll.DAQmxSetAIADCTimingMode
    if cfunc.argtypes is None:
        with cfunc.arglock:
            if cfunc.argtypes is None:
                cfunc.argtypes = [
                    lib_importer.task_handle, ctypes_byte_str,
                    ctypes.c_int]

    error_code = cfunc(
        self._handle, channel, sample_mode)
    check_for_error(error_code)

#use this function in your code
self.task.timing.adc_sample_high_speed()