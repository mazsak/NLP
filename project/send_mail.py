from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QScrollArea

from mail import Mail


class DetailsMail(QScrollArea):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)

        layout: QVBoxLayout = QVBoxLayout()

        self.addressee: QLabel = QLabel()
        self.addressee.setWordWrap(True)
        self.subject: QLabel = QLabel()
        self.subject.setWordWrap(True)
        self.contents: QLabel = QLabel()
        self.contents.setWordWrap(True)

        layout.addWidget(self.addressee)
        layout.addWidget(self.subject)
        layout.addWidget(self.contents)
        self.setLayout(layout)

    def change_mail(self, mail: Mail) -> None:
        self.addressee.setText(f'{mail.addressee.name} <{mail.addressee.address}>')
        self.subject.setText(mail.subject)
        self.contents.setText(mail.contents)

        self.addressee.repaint()
        self.subject.repaint()
        self.contents.repaint()

    def delete_data(self):
        self.addressee.setText('')
        self.subject.setText('')
        self.contents.setText('')

        self.addressee.repaint()
        self.subject.repaint()
        self.contents.repaint()
