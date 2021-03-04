from Circle import Circle


class Car(Circle):

    def __init__(self, x, y, connection):
        Circle.__init__(self, x, y, 100)
        self.connection = connection

    def set_circle(self, circle):
        self.x = circle.x
        self.y = circle.y
        self.radius = circle.radius

    def drive_forward(self):
        string = "1"
        self.connection.write((string.encode()))

    def turn_left(self):
        string = "2"
        self.connection.write((string.encode()))

    def turn_right(self):
        string = "3"
        self.connection.write((string.encode()))

    def stop(self):
        string = "4"
        self.connection.write((string.encode()))
