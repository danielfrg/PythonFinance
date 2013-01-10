from finance.events import Condition

def decrease(decrease):
    condition = Condition()
    condition.id = 'decrease' + str(decrease)
    condition.function = lambda i, item, data: (data[i-1] - item > decrease)
    return condition

def increase(increase):
    condition = Condition()
    condition.id = 'increase' + str(increase)
    condition.function =  lambda i, item, data: (item - data[i-1] > increase)
    return condition

def went_below(below):
    condition = Condition()
    condition.id = 'went_below' + str(below)
    condition.function = lambda i, item, data: (data[i-1] >= below and item < below)
    return condition

def went_above(above):
    condition = Condition()
    condition.id = 'went_above' + str(above)
    condition.function = lambda i, item, data: (data[i-1] <= above and item > above)
    return condition