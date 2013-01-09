

class Event(object):
    def __init__(self):
        self.id = None
        self.function = Event.default

    @staticmethod
    def default(i, item, data):
        raise Exception('Event.function needs to be written')