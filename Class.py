class User:
    def __init__(self, pic, content):
        self.pic = pic
        self.content = content

    def __repr__(self):
        return f'{self.pic} \n {self.content}'
