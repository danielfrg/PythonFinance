from finance.events import Event

def decrease(decrease):
    event = Event()
    event.id = 'decrease' + str(decrease)
    event.function = lambda i, item, data: (data[i-1] - item > decrease)
    return event

def increase(increase):
    event = Event()
    event.id = 'increase' + str(increase)
    event.function =  lambda i, item, data: (item - data[i-1] > increase)
    return event

def went_below(below):
    event = Event()
    event.id = 'went_below' + str(below)
    event.function = lambda i, item, data: (data[i-1] >= below and item < below)
    return event

def went_above(above):
    event = Event()
    event.id = 'went_above' + str(above)
    event.function = lambda i, item, data: (data[i-1] <= above and item > above)
    return event