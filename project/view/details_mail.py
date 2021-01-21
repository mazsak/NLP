import functools
import json

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QScrollArea, QHBoxLayout, QWidget, QPushButton

from api_mail import ApiMail
from model.mail import Mail


class DetailsMail(QScrollArea):

    def __init__(self, api: ApiMail, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)

        with open('responses.json', 'r') as f:
            self.responses = json.load(f)

        self.layout: QVBoxLayout = QVBoxLayout()
        self.buttons: list = []
        self.addressee: QLabel = QLabel()
        self.addressee.setWordWrap(True)
        self.subject: QLabel = QLabel()
        self.subject.setWordWrap(True)
        self.contents: QLabel = QLabel()
        self.contents.setWordWrap(True)
        self.api_mail = api

        self.layout.addWidget(self.addressee)
        self.layout.addWidget(self.subject)
        self.layout.addWidget(self.contents)
        self.setLayout(self.layout)

    def change_mail(self, mail: Mail) -> None:
        self.addressee.setText(f'{mail.addressee.name} <{mail.addressee.address}>')
        self.subject.setText(mail.subject)
        self.contents.setText(mail.contents)

        for button in self.buttons:
            self.layout.removeWidget(button)
        self.buttons = []
        for category in mail.category:
            if category in self.responses.keys():
                for response in self.responses[category]:
                    button: QPushButton = QPushButton(response)
                    button.clicked.connect(functools.partial(self.__send, mail, response))
                    self.buttons.append(button)
                    self.layout.addWidget(button)

        self.repaint()

    def delete_data(self):
        self.addressee.setText('')
        self.subject.setText('')
        self.contents.setText('')

        self.addressee.repaint()
        self.subject.repaint()
        self.contents.repaint()

    def __send(self, mail, response):
        my_mail: Mail = Mail(recipient=mail.recipient, addressee=mail.addressee, contents=response, subject=mail.category, id=bytes())
        self.api_mail.send(mail=my_mail)
