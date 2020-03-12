class Comment:
    def __init__(self, minute, time, img, text):
        self.minute = minute
        self.time = time
        self.img = img
        self.text = text

    def __str__(self):
        return "{minute: " + self.minute + ";\ntime: " + self.time + ";\nimg: " + self.img + ";\ntext: " + self.text \
               + "}"
