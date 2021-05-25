import cv2
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QPushButton, QVBoxLayout, QLineEdit, QLabel
from PIL import Image
from utility import crypt, decrypt


class App(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout()

        self.filename = None

        self.button = QPushButton("Load Image")
        self.button.clicked.connect(self.get_file)

        self.encrypt_button = QPushButton("Encrypt Image")
        self.encrypt_button.clicked.connect(self.encrypt)

        self.decrypt_button = QPushButton("Decrypt Image")
        self.decrypt_button.clicked.connect(self.decrypt)

        self.message_label = QLabel(self)
        self.message_label.setText("Enter secret message:")

        self.messageBox = QLineEdit(self)
        self.messageBox.textChanged.connect(self.text_changed)
        self.message = None

        self.output_label = QLabel(self)

        layout.addWidget(self.message_label)
        layout.addWidget(self.messageBox)
        layout.addWidget(self.button)
        layout.addWidget(self.encrypt_button)
        layout.addWidget(self.decrypt_button)
        layout.addWidget(self.output_label)

        self.setLayout(layout)
        self.setWindowTitle("Steganography")
        self.show()

    def get_file(self):
        self.filename = QFileDialog.getOpenFileName(self, 'Open file', 'c:\\', "Image files (*.jpg *.png)")[0]

    def save_file(self, content):
        self.filename = QFileDialog.getSaveFileName(self, 'Save File')[0]
        content.save(self.filename)

    def text_changed(self):
        self.message = self.messageBox.text()

    def encrypt(self):
        img = Image.open(self.filename)
        self.save_file(crypt(img, bytes(self.message, 'ascii')))

    def decrypt(self):
        img = Image.open(self.filename)
        self.output_label.setText(decrypt(img))

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    window = App()
    sys.exit(app.exec_())
