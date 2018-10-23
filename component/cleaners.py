import time


class BaseCleaner(object):
    def __init__(self, *args, **kwargs):
        pass

    def clean_data(self,market_code, symbol, data):
        raise NotImplementedError("this method must override")


class BinanceDepthCleaner(BaseCleaner):
    def __init__(self, *args, **kwargs):
        super(BinanceDepthCleaner, self).__init__(*args, **kwargs)

    def clean_data(self, market_code, symbol, data):
        data["asks"] = [[ask[0], str(ask[1])] for ask in data["asks"]]
        data["bids"] = [[bid[0], str(bid[1])] for bid in data["bids"]]
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
            """
            trade_type = trade.pop("isBestMatch")
            if trade_type is True:
                trade["type"] = "market"
            else:
                trade["type"] = "limit"
            """
        return data

class HuobiDepthCleaner(BaseCleaner):
    def __init__(self, *args, **kwargs):
        super(HuobiDepthCleaner, self).__init__(*args, **kwargs)

    def clean_data(self,market_code, symbol, data):
        return data["tick"]


class HuobiTradeCleaner(BaseCleaner):
    def __init__(self,*args, **kwargs):
        super(HuobiTradeCleaner, self).__init__(*args, **kwargs)

    def clean_data(self,market_code, symbol, data):
        all_data = data["data"]
        clean_data = []
        for trade in all_data:
            for i in trade["data"]:
                child_data = {
                    "market_code":market_code, "symbol": symbol, "amount": i["amount"],
                    "order_id": i["id"], "price": i["price"], "side": i["direction"],
                    "time": i["ts"]
                }
                clean_data.append(child_data)

        return clean_data


class ZBDepthCleaner(BaseCleaner):
    def __init__(self, *args, **kwargs):
        super(ZBDepthCleaner, self).__init__(*args, **kwargs)

    def clean_data(self,market_code, symbol, data):
        return data


class ZBTradeCleaner(BaseCleaner):
    def __init__(self, *args, **kwargs):
        super(ZBTradeCleaner, self).__init__(*args, **kwargs)

    def clean_data(self,market_code, symbol, data):
        for trade in data:
            trade["market_code"] = market_code
            trade["symbol"] = symbol
            ts = trade.pop("date") * 1000
            trade["time"] = ts
            trade["order_id"] = trade.pop("tid")
            trade["side"] = trade.pop("type")
            trade.pop("trade_type")
        return data


class HitBTCDepthCleaner(BaseCleaner):
    def __init__(self, *args, **kwargs):
        super(HitBTCDepthCleaner, self).__init__(*args, **kwargs)

    def clean_data(self,market_code, symbol, data):
        return data


class HitBTCTradeCleaner(BaseCleaner):
    def __init__(self, *args, **kwargs):
        super(HitBTCTradeCleaner, self).__init__(*args, **kwargs)

    def clean_data(self,market_code, symbol, data):
        trade_data = data["trades"]
        return_data = []
        for trade in trade_data:
            child_data = {
                "market_code": market_code, "symbol": symbol, "order_id": trade[0],
                "price": trade[1], "amount": trade[2], "time": trade[3]
            }
            if trade[2] > 0:
                child_data["side"] = "buy"
            else:
                child_data["side"] = "sell"
            return_data.append(child_data)
        return return_data


class OKEXDepthCleaner(BaseCleaner):
    def __init__(self, *args, **kwargs):
        super(OKEXDepthCleaner, self).__init__(*args, **kwargs)

    def clean_data(self,market_code, symbol, data):
        return data


class OKEXTradeCleaner(BaseCleaner):
    def __init__(self, *args, **kwargs):
        super(OKEXTradeCleaner, self).__init__(*args, **kwargs)

    def clean_data(self,market_code, symbol, data):
        for trade in data:
            trade["time"] = trade.pop("date_ms")
            trade["order_id"] = trade.pop("tid")
            trade["side"] = trade.pop("type")
            trade["market_code"] = market_code
            trade["symbol"] = symbol
            trade.pop("date")
        return data


class OKCoinDepthCleaner(BaseCleaner):
    def __init__(self, *args, **kwargs):
        super(OKCoinDepthCleaner, self).__init__(*args, **kwargs)

    def clean_data(self,market_code, symbol, data):
        return data


class OKCoinTradeCleaner(BaseCleaner):
    def __init__(self, *args, **kwargs):
        super(OKCoinTradeCleaner, self).__init__(*args, **kwargs)

    def clean_data(self,market_code, symbol, data):
        for trade in data:
            trade["time"] = trade.pop("date_ms")
            trade["order_id"] = trade.pop("tid")
            trade["side"] = trade.pop("type")
            trade["market_code"] = market_code
            trade["symbol"] = symbol
            trade.pop("date")
        return data


class PoloniexDepthCleaner(BaseCleaner):
    def __init__(self, *args, **kwargs):
        super(PoloniexDepthCleaner, self).__init__(*args, **kwargs)

    def clean_data(self,market_code, symbol, data):
        data.pop("isFrozen")
        data.pop("seq")
        data["asks"] = [[ask[0],str(ask[1])] for ask in data["asks"]]
        data["bids"] = [[bid[0], str(bid[1])] for bid in data["bids"]]
        return data


class PoloniexTradeCleaner(BaseCleaner):
    def __init__(self, *args, **kwargs):
        super(PoloniexTradeCleaner, self).__init__(*args, **kwargs)

    def clean_data(self,market_code, symbol, data):
        return_data = []
        for trade in data:
            record = [
                int(time.mktime(time.strptime(trade.pop("date"), '%Y-%m-%d %H:%M:%S')) * 1000),
                trade["tradeID"], trade["rate"], trade["amount"], trade["type"]
            ]
            return_data.append(record)
        return_data.reverse()
            # trade["side"] = trade.pop("type")
            # trade["price"] = trade.pop("rate")
            # trade["market_code"] = market_code
            # trade["symbol"] = symbol
            # trade["order_id"] = -1
            # trade["time"] = time.mktime(time.strptime(trade.pop("date"), '%Y-%m-%d %H:%M:%S')) * 1000
            # trade.pop("total")


        return return_data
