

class Condition(object):
    def __init__(self):
        self.id = None
        self.function = Condition.default

    @staticmethod
    def default(i, item, data):
        raise Exception('Condition.function needs to be written')