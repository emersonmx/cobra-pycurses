class Private(object):

    def __init__(self):
        super(Private, self).__init__()

        self._private_attribute = 42
        self.public_attribute = 64

def _private_function():
    print "private"
