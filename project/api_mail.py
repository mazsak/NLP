import email
import imaplib
import smtplib
from mailbox import Message
from typing import Union, List

from addressee import Addressee
from mail import Mail


class ApiMail:

    def __init__(self, user: str, password: str, server_name: str, port: int) -> None:
        self.user = user
        self.password = password
        self.server_name = server_name
        self.port = port
        self.server: Union[smtplib.SMTP_SSL, None] = None
        self.mail: Union[imaplib.IMAP4_SSL, None] = None

    def login(self) -> bool:
        try:
            self.server: smtplib.SMTP_SSL = smtplib.SMTP_SSL(self.server_name, self.port)
            self.server.login(self.user, self.password)

            self.mail: imaplib.IMAP4_SSL = imaplib.IMAP4_SSL(self.server_name)
            self.mail.login(self.user, self.password)
            self.mail.select('inbox')

            return True
        except Exception as e:
            print(e)
            return False

    def send(self, mail: Mail) -> None:
        pass

    def download(self) -> List[Mail]:
        self.mail.select('inbox')
        status, data = self.mail.search(None, 'ALL')
        mails: List[Mail] = []
        if status == 'OK':
            ids = []
            for block in data:
                ids += block.split()

            for i in ids:
                status, data = self.mail.fetch(i, '(RFC822)')

                if status == 'OK':
                    for response_part in data:
                        if isinstance(response_part, tuple):
                            message: Message = email.message_from_bytes(response_part[1])

                            mail_content: str = ''
                            if message.is_multipart():

                                for part in message.get_payload():
                                    if part.get_content_type() == 'text/plain':
                                        mail_content += part.get_payload()
                            else:
                                mail_content = message.get_payload()
                            mail: Mail = Mail(id=i, addressee=Addressee(message['from']), recipient=message['to'],
                                              subject=message['subject'], contents=mail_content, date=message['date'])
                            mails.append(mail)
        return mails

    def delete(self, id: bytes) -> None:
        self.mail.store(id, '+FLAGS', '\\Deleted')
        self.mail.expunge()
