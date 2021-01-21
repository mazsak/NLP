from PyQt5.QtWidgets import QVBoxLayout, QLineEdit, QPlainTextEdit, QDialog, \
    QDialogButtonBox

from api_mail import ApiMail
from model.addressee import Addressee
from model.mail import Mail


class SendMail(QDialog):

    def __init__(self, api_mail: ApiMail, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.setWindowTitle("Send mail")

        self.api_mail: ApiMail = api_mail

        layout: QVBoxLayout = QVBoxLayout()

        self.addressee: QLineEdit = QLineEdit(self)
        self.addressee.setPlaceholderText('Addressee')
        self.subject: QLineEdit = QLineEdit(self)
        self.subject.setPlaceholderText('Subject')
        self.contents: QPlainTextEdit = QPlainTextEdit(self)
        self.contents.setPlaceholderText('Contents')
        buttons = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        button_box = QDialogButtonBox(buttons)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        layout.addWidget(self.addressee)
        layout.addWidget(self.subject)
        layout.addWidget(self.contents)
        layout.addWidget(button_box)

        self.setLayout(layout)

    def send(self) -> None:
        mail: Mail = Mail(recipient=self.api_mail.user, addressee=Addressee(f'<{self.addressee.text()}>'),
                          contents=self.contents.toPlainText(), subject=self.subject.text(), id=bytes())
        self.api_mail.send(mail)
