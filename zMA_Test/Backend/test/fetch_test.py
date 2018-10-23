
def rating_func(x):
    '''
    red word = -1
    yellow word = +0.5
    green word = +1
    :param x: function
    :return: value between 1 and 10
    '''
    a = 1
    b = 10
    max = 500  #negative number of users
    min = -500  #positive number of users
    return (((b-a)*(x-min))/(max-min)) + a

