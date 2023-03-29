import serial, serial.tools.list_ports
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from threading import Thread, Event

class Function_UI(QObject):
    data_available = pyqtSignal(str)
    def __init__(self):
        super().__init__()

        self.serialPort = serial.Serial()
        # self.serialPort.timeout = 0.5

        self.baudList = {
            '4800':4800,
            '9600':9600,
            '19200':19200,
            '38400':38400,
            '115200':115200
        }
        self.portList = []
        self.thread = None
        self.alive = Event()

    def update_port(self):
        self.portList = [port.device for port in serial.tools.list_ports.comports()]
    
    def connect_serial(self):
        try:
            self.serialPort.open()
            if(self.serialPort.is_open):
                self.start_thread()
        except:
            print('Connect warning!')
    
    
    def read_serial(self):
        while (self.alive.isSet() and self.serialPort.is_open):
            try:
                data = self.serialPort.readline().decode("utf-8").strip()
                if(len(data)>1):
                    self.data_available.emit(data)
                print(data)
            except:
                pass
        
    # def send_data(self, data):
    #     if(self.serialPort.is_open):
    #         messages = str(data) + "\n"
    #         self.serialPort.write(messages.encode())


    def start_thread(self):
        self.thread = Thread(target = self.read_serial)
        self.thread.setDaemon(1)
        self.alive.set()
        self.thread.start()
    
    def stop_thread(self):
        if(self.thread is not None):
            self.alive.clear()
            self.thread.join()
            self.thread = None
