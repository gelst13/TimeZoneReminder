class Smth:
    def __init__(self):
        self.contact_name = 'asdf'
        self.location = 'RU'

    def __repr__(self):
        return '<Contact {} from {}>'.format(self.contact_name, self.location)


new = Smth()
print(new)
