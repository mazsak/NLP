from typing import List

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QHBoxLayout, QWidget, QLabel, QVBoxLayout, QPushButton

from api_mail import ApiMail
from details_mail import DetailsMail
from list_email import ListEmail
from mail import Mail

StyleSheep = """
QPushButton{
    border: none;
    background-color: #1a1a1a; 
    color: white;
    padding: 5px;
}
QPushButton:hover{
    background-color: #262626;
}
QScrollBar:horizontal {
    background-color: #333333;
    color: #333333;
    height: 5px;
}
QScrollBar::handle:horizontal {
    background-color: #262626;
}
QScrollBar::handle::pressed:horizontal {
    background-color : #1a1a1a;
    border: 3px solid #262626;
}
QScrollBar:vertical {
    background-color: #333333;
    color: #333333;
    width: 5px;
}
QScrollBar::handle:vertical {
    background-color: #262626;
}
QScrollBar::handle::pressed:vertical {
    background-color : #1a1a1a;
    border: 3px solid #262626;
}
QLabel {
    color: white;
    font-size: 12px;
}
QListWidget { 
    border: none; 
    background-color: #1a1a1a;
} 
QListWidget::item { 
    border: 1px solid #1a1a1a; 
    background-color:  #333333;
}
QScrollArea, QMainWindow {
    background-color: #1a1a1a; 
    color: white;
    border: none;
}
"""


class Window(QMainWindow):

    def __init__(self, api: ApiMail) -> None:
        super().__init__()
        self.setStyleSheet(StyleSheep)
        self.setMinimumSize(1000, 500)
        self.setWindowTitle('EMAIL')

        self.api = api
        mails: List[Mail] = self.api.download()

        layout: QHBoxLayout = QHBoxLayout()

        self.details_email: DetailsMail = DetailsMail()
        self.list_email: ListEmail = ListEmail(mails=mails, details=self.details_email)

        user: QLabel = QLabel(api.user)
        user.setStyleSheet('font-size:18px; font-weight: bold; margin:10px; background-color:red;')
        user.setMaximumWidth(350)

        v_layout: QVBoxLayout = QVBoxLayout()
        v_layout.setSizeConstraint(350)

        v_layout.addWidget(user)
        v_layout.addWidget(self.__init_tool_bar())
        v_layout.addWidget(self.list_email)

        w: QWidget = QWidget()
        w.setLayout(v_layout)

        layout.addWidget(w)
        layout.addWidget(self.details_email)

        widget: QWidget = QWidget()
        widget.setLayout(layout)

        self.setCentralWidget(widget)

        self.show()

    def __init_tool_bar(self) -> QWidget:
        layout: QHBoxLayout = QHBoxLayout()
        layout.setSizeConstraint(350)

        send: QPushButton = QPushButton(self)
        send.setIcon(QIcon('add.png'))
        send.clicked.connect(self.send_mails)
        send.setFixedWidth(115)

        refresh: QPushButton = QPushButton(self)
        refresh.setIcon(QIcon('refresh.png'))
        refresh.clicked.connect(self.refresh_mails)
        refresh.setFixedWidth(115)

        trash: QPushButton = QPushButton(self)
        trash.setIcon(QIcon('trash.png'))
        trash.clicked.connect(self.delete_selected_mail)
        trash.setFixedWidth(115)

        layout.addWidget(send)
        layout.addWidget(refresh)
        layout.addWidget(trash)

        w: QWidget = QWidget()
        w.setLayout(layout)
        w.setFixedWidth(345)

        return w

    def delete_selected_mail(self) -> None:
        mails: List[Mail] = self.list_email.get_item_checked()
        for mail in mails:
            self.api.delete(mail.id)

        self.refresh_mails()

    def refresh_mails(self) -> None:
        mails: List[Mail] = self.api.download()
        self.list_email.refresh(mails)

    def send_mails(self):

        pass
