import websockets
import json
import time
import asyncio
import gzip

class websocket_utils:
    def __init__(self):
        self.topics = []
        self.hidden_topics = []
        self.URL="wss://stream.bybit.com/v5/public/spot"
        self.HIDDEN_URL=f"wss://ws2.bybit.com/spot/ws/quote/v2?_platform=2&timestamp={time.time()}"
        
    async def ws_send(self, message, websocket):
        """
        Args:
            message (str): {"op": "", 
                            "args": ""}...
        """
        await websocket.send(json.dumps(message))
        
    
    async def ws_ping(self, interval, websocket):
        while True:
            msg = {"op": "ping", "args": [time.time()]}
            await self.ws_send(websocket=websocket, message=msg)
            await asyncio.sleep(interval)

        
    async def subscribe(self, queue, is_hidden=False, subscribe_message=''):
        """Подписка на WebSocket с автоматическим переподключением."""
        
        while True:
            try:
                if is_hidden:
                    self.URL = self.HIDDEN_URL
                    self.topics = self.hidden_topics
                
                async with websockets.connect(self.URL) as websocket:
                    if is_hidden:
                        ping_task = asyncio.create_task(self.ws_ping(interval=15, websocket=websocket))
                        
                        if "mergedDepth" in self.topics[0]:
                            subscribe_message = {
                                "topic": self.topics[0].split('.')[0].split("_")[0], 
                                "symbol": self.topics[0].split('.')[-1].split(':')[0],
                                "params": {
                                    "binary": False,
                                    "dumpScale": self.topics[0].split(':')[1].split('=')[1],
                                    "limit": int(self.topics[0].split('.')[0].split("_")[1]),
                                },
                                "event": "sub"
                            }
                        elif "kline" in self.topics[0]:
                            subscribe_message = {
                                "topic": self.topics[0].split('.')[0],
                                "params": {"binary": False, "limit": 1},
                                "symbol": self.topics[0].split('.')[-1],
                                "event": "sub"
                            }
                    else:
                        subscribe_message = {
                            "op": "subscribe",
                            "args": self.topics
                        }

                    await websocket.send(json.dumps(subscribe_message))
                    print(f"Subscribed to channels: {self.topics}")

                    while True:
                        response = await websocket.recv() 
                        
                        if is_hidden:
                            if isinstance(response, str):
                                await queue.put(json.loads(response))
                            elif isinstance(response, bytes):
                                decompressed_data = gzip.decompress(response)
                                decoded_text = decompressed_data.decode("utf-8")
                                json_data = json.loads(decoded_text)
                                await queue.put(json_data)
                        else:
                            await queue.put(json.loads(response))

            except (websockets.ConnectionClosed, asyncio.TimeoutError, OSError) as e:
                print(f"WebSocket connection lost: {e}, attempting to reconnect...")
                await asyncio.sleep(5)

        pass
    
    
