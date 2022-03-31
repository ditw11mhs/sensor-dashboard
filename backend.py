import serial
import time

class SerialHandler:
    def __init__(self, port, baudrate, timeout):
        self.ser = serial.Serial(port=port, baudrate=baudrate, timeout=timeout)

    def readline(self):
        time.sleep(0.001)
        return self.ser.readline()

    def preprocess(self, data):
        raw_dat = data.decode()
        data = raw_dat.strip()
        return [float(x) for x in data.split("|")]

    def preprocess_readline(self):
        data = self.readline()
        return self.preprocess(data)
