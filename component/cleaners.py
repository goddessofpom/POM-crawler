class BaseCleaner(object):
    def __init__(self, *args, **kwargs):
        pass

    def clean_data(self,market_code, symbol, data):
        raise NotImplementedError("this method must override")


class BinanceDepthCleaner(BaseCleaner):
    def __init__(self, *args, **kwargs):
        super(BinanceDepthCleaner, self).__init__(*args, **kwargs)

    def clean_data(self, market_code, symbol, data):
        return data

class BinanceTradeCleaner(BaseCleaner):
    def __init__(self, *args, **kwargs):
        super(BinanceTradeCleaner, self).__init__(*args, **kwargs)

    def clean_data(self, market_code, symbol, data):
        for trade in data:
            trade["market_code"] = market_code
            trade["symbol"] = symbol
            trade["amount"] = trade.pop("qty")
            trade["order_id"] = trade.pop("id")
            side = trade.pop("isBuyerMaker")
            if side is True:
                trade["side"] = "buy"
            else:
                trade["side"] = "sell"
            trade_type = trade.pop("isBestMatch")
            if trade_type is True:
                trade["type"] = "market"
            else:
                trade["type"] = "limit"
        return data
