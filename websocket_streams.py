from bybit_python.utils.websocket_utils import websocket_utils

class websocket_streams:
    def __init__(self, url, market):
        """_summary_

        Args:
            url (_type_): _description_
            market (_type_): _description_
        """
        self.topic = None
        self.PUBLIC_URL= f"{url}/piblic/{market}"
        self.utils = websocket_utils()
    
    async def sub_orderbook(self, symbol, depth):
        """_summary_

        Args:
            symbol (_type_): _description_
            depth (_type_): _description_
        """
        topic = f"orderbook.{depth}.{symbol}"
        self.utils.topics.append(topic)
        print(self.utils.topics)

    
    async def sub_trade(self, symbol):
        topic = f"publicTrade.{symbol}"
        self.utils.topics.append(topic)

    
    async def sub_kline(self, symbol, topic=""):
        pass
    
    async def sub_candle(self, interval, symbol):
        """_summary_
        WARNING: This is a hidden func of API. that Use not defaut api URL: f"wss://ws2.bycbe.com/realtime_w?timestamp={time.time()}"
        return something like:

        Args:
            interval (str): 1s 
            symbol (str): f.ex BTCUSDT 
        """
        topic = f"kline_{interval}.{symbol}"
        self.utils.hidden_topics.append(topic)
    
    async def sub_ticker(self, symbol, topic=""):
        pass
    