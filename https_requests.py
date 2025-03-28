from bybit_python.utils.https_utils import https_utils

class https_requests(https_utils):
    def __init__(self, istestnet=False):
        super().__init__(istestnet)
        
    async def kline_history(self, symbol, interval, start, end, category='spot', limit="200"):
        return await super().https_request(path="market/kline", 
                                           params={"category":category, 
                                                    "symbol": symbol, 
                                                    "interval": interval,
                                                    "start": str(start) + "000",
                                                    "end": str(end) + "000",
                                                    "limit": limit})
        