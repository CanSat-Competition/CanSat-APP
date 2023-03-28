

# dic = {"GPS1":179,"GPS2":145,"GYRO":{"x":7.6,"y":6.3},"Temp":2.3,"IVME":15,"HIZ":56,"NEM":46,"TEZYIQ":{"GY":527,"T":345},"HATALAR":{"1":1,"2":1,"3":1,"4":0,"5":1},"SAAT":{"REALTIME":57,"START":58,"LEAVE":33,"DOWN":4,"TOPLAM":37}}

# print(dic.get('GPS1'))


# import serial

# ser = serial.Serial('/dev/ttyACM0', 9600)

# while True:
#     data = ser.readline().decode('utf-8').rstrip() # Veriyi okuyun ve kodlamayı ayarlayın
#     print(data) # Veriyi yazdırın

from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QGraphicsView, QGraphicsProxyWidget
from PyQt5.QtChart import QChart, QChartView, QLineSeries
from PyQt5.QtGui import QPainter
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create a line series
        series = QLineSeries()
        series.append(0, 1)
        series.append(1, 3)
        series.append(2, 4)
        series.append(3, 2)
        series.append(4, 5)

        # Create a chart and add the line series to it
        chart = QChart()
        chart.addSeries(series)

        # Set the title and axes labels
        # chart.setTitle("Line Chart")
        chart.setAnimationOptions(QChart.SeriesAnimations)
        chart.createDefaultAxes()

        # Set the minimum size of the chart
        chart.setMinimumSize(800, 600)

        # Create a chart view and set the chart as its model
        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.Antialiasing)

        # Create a graphics proxy widget and set the chart view as its widget
        proxy = QGraphicsProxyWidget()
        proxy.setWidget(chart_view)

        # Create a graphics scene and add the proxy widget to it
        scene = QGraphicsScene(self)
        scene.addItem(proxy)

        # Create a graphics view and set the graphics scene as its model
        graphics_view = QGraphicsView(scene)
        self.setCentralWidget(graphics_view)

        # Set the window size and show the window
        self.setGeometry(100, 100, 800, 600)
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())