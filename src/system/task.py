class Tasks:
    def __init__(self):
        self.list_xy = []
        self.size = 0

    def put(self, element):
        self.list_xy.append(element)
        self.size += 1

    def get(self):
        element = self.list_xy.pop(0)
        self.size -= 1
        return element

    def empty(self):
        if self.size == 0:
            return True
        else:
            return False
