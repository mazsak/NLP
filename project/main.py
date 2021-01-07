import sys

from PyQt5.QtWidgets import QApplication

from api_mail import ApiMail
from window import Window

server_name = 'smtp.gmail.com'
user = 'nlp.app.project@gmail.com'
password = 'nlpa1234'
port = 465
if __name__ == '__main__':
    api: ApiMail = ApiMail(user, password, server_name, port)
    api.login()
    app = QApplication(sys.argv)
    ex = Window(api)
    sys.exit(app.exec_())
