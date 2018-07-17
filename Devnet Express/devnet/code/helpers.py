""" Helpers module """

def curry(func, variable):
    """ Returns a partially invokable function. """
    second = variable
    def function(first):
        """ Invoke partially invokable function """
        return func(first, second)
    return function
