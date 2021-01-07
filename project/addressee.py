class Addressee:

    def __init__(self, data: str):
        self.name: str = data.split('<')[0].strip()
        self.address = data[data.find('<') + 1: data.find('>')]

    def __repr__(self):
        return f'<Addressee: name: {self.name}, address: {self.address}>'

    def __str__(self):
        return f'<Addressee: name: {self.name}, address: {self.address}>'
