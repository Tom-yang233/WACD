import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QLabel, QPushButton, QFileDialog, QLineEdit, QGridLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from tx import tx_pic


class TxApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Wireless Audio Communication Demonstration-Transmitter")
        self.img_path = None
        self.init_ui()

    def init_ui(self):
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.resize(1080,1920)

        self.load_button = QPushButton('Load Image', self)
        self.load_button.clicked.connect(self.load_image)

        self.param1_label = QLabel('Rate', self)
        self.param1_edit = QLineEdit(self)
        self.param1_edit.setText('176400')


        self.param2_label = QLabel('Chunk', self)
        self.param2_edit = QLineEdit(self)
        self.param2_edit.setText('20000')

        self.param3_label = QLabel('Amplitude', self)
        self.param3_edit = QLineEdit(self)
        self.param3_edit.setText('4096')

        self.tx_button = QPushButton('Tx', self)
        self.tx_button.clicked.connect(self.tx_img)

        layout = QGridLayout()
        layout.addWidget(self.image_label,0,0)
        layout.addWidget(self.load_button,0,1)
        layout.addWidget(self.tx_button,1,1)
        layout.addWidget(self.param1_label,3,1)
        layout.addWidget(self.param1_edit,3,2)
        layout.addWidget(self.param2_label,4,1)
        layout.addWidget(self.param2_edit,4,2)
        layout.addWidget(self.param3_label,5,1)
        layout.addWidget(self.param3_edit,5,2)

        self.setLayout(layout)

    def load_image(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setNameFilter("Images (*.png *.jpg *.bmp *.gif)")
        file_dialog.setViewMode(QFileDialog.Detail)

        if file_dialog.exec_():
            selected_file = file_dialog.selectedFiles()[0]
            self.img_path = selected_file
            self.display_image(selected_file)

    def display_image(self, image_path):
        pixmap = QPixmap(image_path)
        self.image_label.setPixmap(pixmap.scaled(640,480, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        # self.image_label.setPixmap(pixmap)

    def tx_img(self):
        if self.img_path is not None:
            tx_pic(file_path=self.img_path, RATE=int(self.param1_edit.text()), _CHUNK=int(self.param2_edit.text()), AMPLITUDE=int(self.param3_edit.text()))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TxApp()
    window.setGeometry(100, 100, 800, 600)
    window.show()
    sys.exit(app.exec_())