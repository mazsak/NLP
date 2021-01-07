from datetime import datetime
from typing import List

from addressee import Addressee

months: List[str] = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


class Mail:

    def __init__(self, id: bytes, addressee: Addressee, recipient: str = '', subject: str = '', contents: str = '',
                 date: str = '') -> None:
        self.id: bytes = id
        self.addressee: Addressee = addressee
        self.recipient: str = recipient
        self.subject: str = subject
        self.contents: str = contents
        if date == '':
            self.date: datetime = datetime.now()
        else:
            date = date.replace(':', " ").replace(',', '').split(" ")
            self.date: datetime = datetime(day=int(date[1]), month=months.index(date[2]) + 1, year=int(date[3]),
                                           hour=int(date[4]), minute=int(date[5]), second=int(date[6]))

    def __str__(self) -> str:
        return f'<Mail: id: {self.id}, addressee: {self.addressee}, recipient: {self.recipient}, subject: {self.subject}, contents: {self.contents}, date: {self.date}>'

    def __repr__(self) -> str:
        return f'<Mail: id: {self.id}, addressee: {self.addressee}, recipient: {self.recipient}, subject: {self.subject}, contents: {self.contents}, date: {self.date}>'
