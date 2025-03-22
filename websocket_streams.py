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
                    {
                        "topic": "candle.1s.BTCUSDT",
                        "data": [
                            {
                                "start": 1742677106,
                                "end": 1742677107,
                                "period": "1s",
                                "open": 83912.1,
                                "close": 83923.3,
                                "high": 83923.3,
                                "low": 83912.1,
                                "volume": "1.874",
                                "turnover": "157268.7425",
                                "confirm": true,
                                "cross_seq": 357864512873,
                                "timestamp": 1742677107560099
                            },
                            {
                                "start": 1742677107,
                                "end": 1742677108,
                                "period": "1s",
                                "open": 83923.3,
                                "close": 83923.2,
                                "high": 83923.3,
                                "low": 83923.2,
                                "volume": "0.035",
                                "turnover": "2937.3144",
                                "confirm": false,
                                "cross_seq": 357864514735,
                                "timestamp": 1742677107560099
                            }
                        ],
                        "timestamp_e6": 1742677107560099
                    }
        Args:
            interval (str): 1s 
            symbol (str): f.ex BTCUSDT 
        """
        topic = f"candle.{interval}.{symbol}"
        self.utils.hidden_topics.append(topic)
    
    async def sub_ticker(self, symbol, topic=""):
        pass
    