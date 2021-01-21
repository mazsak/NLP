from PyQt5.QtWidgets import QWidget, QCheckBox, QLabel, QHBoxLayout, QVBoxLayout

from model.mail import Mail


class ItemMail(QWidget):

    def __init__(self, mail: Mail, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setStyleSheet('background-color: #333333; ')
        self.mail: Mail = mail
        layout: QHBoxLayout = QHBoxLayout()

        self.checkbox: QCheckBox = QCheckBox()
        self.addresseeLabel: QLabel = QLabel(mail.addressee.name + '\n')
        self.addresseeLabel.setWordWrap(True)
        self.addresseeLabel.setMaximumWidth(250)
        self.subjectLabel: QLabel = QLabel(mail.subject + ', (' + ', '.join(mail.category) + ')')
        self.subjectLabel.setWordWrap(True)
        self.subjectLabel.setMaximumWidth(250)

        v_layout: QVBoxLayout = QVBoxLayout()

        v_layout.addWidget(self.addresseeLabel)
        v_layout.addWidget(self.subjectLabel)

        v_widget: QWidget = QWidget()
        v_widget.setLayout(v_layout)

        layout.addWidget(self.checkbox)
        layout.addWidget(v_widget, 1)

        self.setLayout(layout)
