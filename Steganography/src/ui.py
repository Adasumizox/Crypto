import cv2
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QPushButton, QVBoxLayout, QLineEdit, QLabel, QErrorMessage
from PIL import Image
from utility import encrypt, decrypt


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

    def get_file(self) -> None:
        self.filename = QFileDialog.getOpenFileName(self, 'Open file', 'c:\\', "Image files (*.bmp *.png)")[0]

    def save_file(self, content: Image) -> None:
        self.filename = QFileDialog.getSaveFileName(self, 'Save File')[0]
        content.save(self.filename)

    def text_changed(self) -> None:
        self.message = self.messageBox.text()

    def encrypt(self) -> None:
        img = Image.open(self.filename)
        try:
            encrypted_img = encrypt(img, bytes(self.message, 'ascii'))
            self.save_file(encrypted_img)
        except:
            msg = QErrorMessage()
            msg.showMessage("Unsupported file format/extension")

    def decrypt(self) -> None:
        img = Image.open(self.filename)
        try:
            decrypted_img = decrypt(img)
            self.output_label.setText(decrypted_img)
        except:
            msg = QErrorMessage()
            msg.showMessage("Unsupported file format/extension")

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    window = App()
    sys.exit(app.exec_())
