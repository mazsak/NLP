from typing import List

from PyQt5.QtCore import QModelIndex
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QListWidget, QListWidgetItem

from details_mail import DetailsMail
from item_mail import ItemMail
from mail import Mail


class ListEmail(QWidget):

    def __init__(self, mails: List[Mail], details: DetailsMail, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setFixedWidth(350)

        self.mails: List[Mail] = mails
        self.details = details
        self.layout: QVBoxLayout = QVBoxLayout()
        self.list: QListWidget = QListWidget()
        self.layout.addWidget(self.list)
        self.__set_mails_layout()
        self.setLayout(self.layout)

    def __set_mails_layout(self) -> None:
        for mail in self.mails:
            w: QListWidgetItem = QListWidgetItem()
            ui_mail: ItemMail = ItemMail(mail=mail)
            w.setSizeHint(ui_mail.sizeHint())
            self.list.addItem(w)
            self.list.setItemWidget(w, ui_mail)
        self.list.clicked.connect(self.go_to_email)
        self.list.repaint()

    def go_to_email(self, index: QModelIndex) -> None:
        item: ItemMail = self.list.indexWidget(index)
        self.details.change_mail(item.mail)

    def get_item_checked(self) -> List[Mail]:
        mails: List[Mail] = []
        for index in range(self.list.count()):
            item: ItemMail = self.list.indexWidget(self.list.indexFromItem(self.list.item(index)))
            if item.checkbox.checkState() == 2:
                mails.append(item.mail)

        return mails

    def refresh(self, mails: List[Mail]) -> None:
        self.mails: List[Mail] = mails
        self.list.clear()
        self.__set_mails_layout()
