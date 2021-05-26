from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QPushButton, QVBoxLayout, QLineEdit, QLabel,\
    QErrorMessage, QCheckBox
from PIL import Image
from utility import encrypt, decrypt
from base64 import urlsafe_b64encode
from cryptography.fernet import Fernet


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

        self.isB64 = False
        self.isFernet = False

        self.c1 = QCheckBox("Base64")
        self.c2 = QCheckBox("Fernet")

        self.c1.stateChanged.connect(self.check_changed1)
        self.c2.stateChanged.connect(self.check_changed2)

        self.output_label = QLabel(self)

        layout.addWidget(self.message_label)
        layout.addWidget(self.messageBox)
        layout.addWidget(self.c1)
        layout.addWidget(self.c2)
        layout.addWidget(self.button)
        layout.addWidget(self.encrypt_button)
        layout.addWidget(self.decrypt_button)
        layout.addWidget(self.output_label)

        self.setLayout(layout)
        self.setWindowTitle("Steganography")
        self.show()

    def get_file(self) -> None:
        self.filename = QFileDialog.getOpenFileName(self, 'Open file', 'c:\\', "Image files (*.bmp *.png *.tiff *.ico)")[0]

    def save_file(self, content: Image) -> None:
        self.filename = QFileDialog.getSaveFileName(self, 'Save File')[0]
        content.save(self.filename)

    def text_changed(self) -> None:
        self.message = self.messageBox.text()

    def encrypt(self) -> None:
        img = Image.open(self.filename)
        try:
            if self.isB64:
                message = urlsafe_b64encode(self.message.encode('ascii'))
            if self.isFernet:
                message = Fernet(Fernet.generate_key()).encrypt(self.message.encode('ascii'))
            else:
                message = bytes(self.message, 'ascii')
            encrypted_img = encrypt(img, message)
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

    def check_changed1(self):
        self.isB64 = not self.isB64

    def check_changed2(self):
        self.isFernet = not self.isFernet

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    window = App()
    sys.exit(app.exec_())
