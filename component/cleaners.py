class BaseCleaner(object):
    def __init__(self, *args, **kwargs):
        pass

    def clean_data(self, data):
        raise NotImplementedError("this method must override")


class BinanceCleaner(BaseCleaner):
    def __init__(self, *args, **kwargs):
        super(BinanceCleaner, self).__init__(*args, **kwargs)

    def clean_data(self, data):
        return data
