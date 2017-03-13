class Card(object):

    def __init__(self, title, text):
        self.title = title
        self.text = text

    def to_dict(self):
        return {title: self.title, text: self.text}
