from PyQt5 import QtWidgets, QtCore
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import sys
import time
import numpy as np
from backend import SerialHandler


class PopUpWindow(QtWidgets.QMainWindow):
    def __init__(self, serial, *args, **kwargs):
        super(PopUpWindow, self).__init__(*args, **kwargs)

        self.serial = serial
        self.graphWidget = pg.PlotWidget()
        self.setCentralWidget(self.graphWidget)

        self.x = np.zeros(100)
        self.y = [np.zeros(100) for i in range(3)]

        self.graphWidget.setBackground("black")
        self.graphWidget.setLabel("left", "Voltage", "V")
        self.graphWidget.setLabel("bottom", "Data", "n")
        self.graphWidget.addLegend()

        pen = [pg.mkPen(color=color, width=3) for color in ["red", "green", "cyan"]]
        name = ["Potentio 1", "Potentio 2", "Potentio 3"]

        self.data_line = [
            self.graphWidget.plot(self.x, self.y[i], pen=pen[i], name=name[i])
            for i in range(3)
        ]

        self.timer = QtCore.QTimer()
        self.timer.setInterval(10)
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()

    def update_plot_data(self):
        start = time.time()
        value = self.serial.preprocess_readline()
        self.x = np.roll(self.x, -1)
        self.x[-1] = self.x[-2] + 1
        for i, data_line in enumerate(self.data_line):
            self.y[i] = np.roll(self.y[i], -1)
            self.y[i][-1] = value[i]
            data_line.setData(self.x, self.y[i])
        print(1 / (time.time() - start))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = PopUpWindow(serial=SerialHandler(port="COM5", baudrate=9600, timeout=0.1))
    w.show()
    sys.exit(app.exec_())
