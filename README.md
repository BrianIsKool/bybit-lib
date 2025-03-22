# self-written lib for bybit

what is this library for? 
1. in defaut lib https://github.com/bybit-exchange/pybit orderbook.{depth}.{symbol} return only Snapshot, but i needed Delta update.
2. bybit has a 'hidden' API and this 'hidden' API has there's a lot of useful stuff like 1s-kline websocket, which has OHLC data in realtime.

2. about websockets: 
    This lib supported defaut bybit API and 'hidden' API.
    API url: "wss://stream.bybit.com/v5/"
    Hidden API url: "wss://ws2.bycbe.com/"
    
usage:.

1. create an asyncio.Queue() and create exemplary class of bybit
2. after that you can subscribe on websocket: `await bbit.websocket.sub_trade(symbol='')`.
   You can  subscribe on many sockets, to do that, just write one more line with sub_*.
   example: ``` await bbit.websocket.sub_trade(symbol='BTCUSDT')
                await bbit.websocket.sub_candle(interval='1s', symbol='BTCUSDT') ```
3. after all socket/s have been added, use `await bbit.subscribe()`, this will sign you up for all the websockets you specify.
4. now you can get info from all sockets in asyncio.Queue, which you set as an argument in first paragraph.
code example: ``` ```


