from datafilter.config import BIG_DEAL_CONFIG


class BigDealFilter(object):
    def __init__(self, redis):
        self.redis = redis

    def _get_big_deal(self, trade):
        coinpair = trade["symbol"].split("/")
        market_code = trade["market_code"]
        exrate_key = "Market_%s_%s_%s" % (market_code, coinpair[0], coinpair[1])
        per_usd = float(self.redis.hget(exrate_key, "USD_price") or 0)
        per_cny = float(self.redis.hget(exrate_key, "CNY_price") or 0)
        cny_price = per_cny * float(trade["amount"])
        usd_price = per_usd * float(trade["amount"])
        if cny_price > BIG_DEAL_CONFIG['amount_limit_cny'] or usd_price > BIG_DEAL_CONFIG['amount_limit_usd']:
            trade['cny_price'] = cny_price
            trade['usd_price'] = usd_price
            return True
        else:
            return False


    def get_useful_data(self, data, timestamp):
        useful_data = [trade for trade in data if trade["time"] > timestamp]
        big_deal_data = list(filter(self._get_big_deal, useful_data))
        save_data = self._pretiffy_data(big_deal_data)
        return save_data

    def _pretiffy_data(self, data):
        pr_data = []
        for trade in data:
            trade_value = (
                trade["timestamp"], trade["symbol"], trade["order_id"], trade["type"],
                trade["market_code"], trade["side"], trade["price"], trade["amount"],
                trade['cny_price'], trade['usd_price']
            )
            pr_data.append(trade_value)
        return pr_data
