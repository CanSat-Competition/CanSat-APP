import ast
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from uart import Ui_MainWindow
from functions import Function_UI
import serial, serial.tools.list_ports
import time

class MainWindow():
    pres_data, temp_data = list(), list() # lists for charts data
    def __init__(self):
        self.main_win = QMainWindow()
        self.uic = Ui_MainWindow()
        self.uic.setupUi(self.main_win)
        self.serial = Function_UI()
        self.serialPort = serial.Serial()
        self.serial.update_port()

        self.uic.portInput.addItems(self.serial.portList)
        self.uic.baudrateInput.addItems(self.serial.baudList)
        self.uic.baudrateInput.setCurrentText('9600')

        # Clickable Buttons   
        self.serial.data_available.connect(self.update_views)
        self.uic.startBtn.clicked.connect(self.connect_or_disconnect)
        self.uic.terminalTextInput.returnPressed.connect(lambda: self.terminal(self.uic.terminalTextInput.text()))

    def update_views(self, data):
        try:
            data = ast.literal_eval(data)
            #Hatalar Güncellenmesi
            errors = data.get('errors')

            error_list = [self.uic.error1, self.uic.error2, self.uic.error3, self.uic.error4]

            for i, error in enumerate(error_list):
                if errors.get(str(i+1)) == 1:
                    error.setStyleSheet("background-color: red;\n"
                                        "border-radius: 5px;\n"
                                        "border-width: 5px;")
                else:
                    error.setStyleSheet("background-color: green;\n"
                                        "border-radius: 5px;\n"
                                        "border-width: 5px;")
                
            #Charts
            def update_chart(chart, list, key):
                value = float(data.get(key))
                list.append(value)
                if len(list) > 50:
                    list.pop(0)
                    chart.clear()
                chart.plot(list, pen="#3BFCCC")
                # chart.setXRange(0,50)

            update_chart(self.uic.preaChart, self.pres_data, "preasure")
            update_chart(self.uic.tempChart, self.temp_data, "temp")
            # End Charts

            # GYRO
            self.uic.xInput.setText(str(data.get('gyro').get('x')))
            self.uic.yInput.setText(str(data.get('gyro').get('y')))
            self.uic.zInput.setText(str(data.get('gyro').get('z')))

            self.uic.x_rotation_angle = data.get('gyro').get('x')
            self.uic.y_rotation_angle = data.get('gyro').get('y')
            self.uic.z_rotation_angle = data.get('gyro').get('z')

            self.uic.mesh_item.rotate(self.uic.y_rotation_angle, 0, 1, 0)
            self.uic.mesh_item.rotate(self.uic.x_rotation_angle, 1, 0, 0)
            self.uic.mesh_item.rotate(self.uic.z_rotation_angle, 0, 0, 1)

            self.uic.x_axis.rotate(self.uic.x_rotation_angle, 1, 0, 0)
            self.uic.x_axis.rotate(self.uic.y_rotation_angle, 0, 1, 0)
            self.uic.x_axis.rotate(self.uic.z_rotation_angle, 0, 0, 1)

            self.uic.y_axis.rotate(self.uic.x_rotation_angle, 1, 0, 0)
            self.uic.y_axis.rotate(self.uic.y_rotation_angle, 0, 1, 0)
            self.uic.y_axis.rotate(self.uic.z_rotation_angle, 0, 0, 1)

            self.uic.z_axis.rotate(self.uic.x_rotation_angle, 1, 0, 0)
            self.uic.z_axis.rotate(self.uic.y_rotation_angle, 0, 1, 0)
            self.uic.z_axis.rotate(self.uic.z_rotation_angle, 0, 0, 1)
            # End GYRO
            
            #Time
            self.uic.clockInput.setText(data.get('clocks').get('realtime'))
            self.uic.startInput.setText(data.get('clocks').get('start_time'))
            self.uic.breakInput.setText(data.get('clocks').get('break_time'))
            self.uic.finishInput.setText(data.get('clocks').get('finish_time'))

            #Speed
            self.uic.speedInput.setText(f"{data.get('speed')} m/s")
            self.uic.speedScreen.setValue(int(data.get('speed')))

            #Height
            self.uic.heightInput.setText(f"{data.get('height')} m")
            self.uic.heightScreen.setValue(int(data.get('height')))

        except:
            print('Loading...')


    def connect_or_disconnect(self):
        if self.uic.startBtn.text() == 'START':
            # if len(Function_UI.data)>0:
            self.connect_serial()
            self.uic.terminalBrowser.append('<span style=\" font-size:8pt; color:#ffffff;\">starting: </span><span style=\" font-size:8pt; color:#00ff00;\">succesfully</span>')
        elif self.uic.startBtn.text() == 'STOP':
            if self.serial.serialPort.is_open:
                self.disconnect_serial()
                self.uic.terminalBrowser.append('<span style=\" font-size:8pt; color:#ffffff;\">stoping: </span><span style=\" font-size:8pt; color:#00ff00;\">succesfully</span>')

    def connect_serial(self):
        port = self.uic.portInput.currentText()
        baud = self.uic.baudrateInput.currentText()
        self.serial.serialPort.port = port
        self.serial.serialPort.baudrate = baud
        self.serial.connect_serial()
        self.uic.startBtn.setText("STOP")
        # IP
        self.uic.ipInput.setEnabled(False)
        # ComboBox
        self.uic.portInput.setEnabled(False)
        self.uic.baudrateInput.setEnabled(False)

    def disconnect_serial(self):
        self.uic.startBtn.setText("START")
        self.serial.stop_thread()
        self.serial.serialPort.close()

        # IP
        self.uic.ipInput.setEnabled(True)
        # ComboBox
        self.uic.portInput.setEnabled(True)
        self.uic.baudrateInput.setEnabled(True)

    def select_file(self, btn):
        options = QFileDialog.Options()
        file_url = QFileDialog.getOpenFileName(None, "QFileDialog.getOpenFileName()", "",
                                                  "All Files (*);", options=options)
        file_name = file_url[0].split("/")[-1]
        self.uic.dosyaAdi.setText(file_name)
        if btn:
            self.uic.terminalBrowser.append(f'<span style=\" font-size:8pt;\">selected: {file_name}</span>')
        return file_name

    def terminal(self, command):

        def setNotficationText(process, p_color, result, r_color):
            notfication = f"""<span style=\" font-size:8pt; color:{p_color};\">{process}: 
                            </span><span style=\" font-size:8pt; 
                            color:{r_color};\">{result}</span>"""
            return notfication
        
        if command == 'ggt -start':
            self.connect_serial()
            self.uic.terminalBrowser.append(setNotficationText('starting', '#ffffff', 'succesfully', '#00ff00'))
        elif command == 'ggt -stop':
            self.disconnect_serial()
            self.uic.terminalBrowser.append(setNotficationText('stoping', '#ffffff', 'succesfully', '#00ff00'))


        self.uic.terminalTextInput.setText('')
    def send_data(self):
        data_send = self.uic.send_Text.toPlainText()
        self.serial.send_data(data_send)

    def update_ports(self):
        self.serial.update_port()
        self.uic.port_List.clear()
        self.uic.port_List.addItems(self.serial.portList)

    def clear(self):
        self.uic.textBrowser.clear()

    def show(self):
        # command to run
        self.main_win.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec())