import sys
import numpy as np
from PyQt5.QtWidgets import QGridLayout
from qtpy.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolBar
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import rx

class RxApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Wireless Audio Communication Demonstration-Receiver")
        self.init_ui()
        self.plot_fig()

    def init_ui(self):
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasQTAgg(self.fig)

        self.rx_button = QPushButton("Rx")

        layout = QGridLayout()
        layout.addWidget(self.canvas, 0, 0)
        layout.addWidget(self.rx_button, 0, 1)

        self.setLayout(layout)

        rx.rx_spectrum()

    def plot_fig(self):
        pass




if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = RxApp()
    window.setGeometry(100, 100, 800, 600)
    window.show()
    sys.exit(app.exec_())