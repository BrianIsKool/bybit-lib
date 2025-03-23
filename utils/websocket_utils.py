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

        
    async def subscribe(self, queue, is_hidden=False):
        """_summary_

        Args:
            queue (_type_): _description_
            url (type): touch this if you know what you are doing! defaut url "wss://stream.bybit.com/v5/public/spot"
        """
        if is_hidden == True:
            self.URL = self.HIDDEN_URL
            self.topics = self.hidden_topics
            
        async with websockets.connect(self.URL) as websocket:
            if is_hidden == True:
                ping_task = asyncio.create_task(self.ws_ping(interval=15, websocket=websocket))
                subscribe_message = {"topic":self.topics[0].split('.')[0],"params":{"binary":False,"limit":1},"symbol":self.topics[0].split('.')[-1],"event":"sub"}
            else:
                subscribe_message = {
                    "op": "subscribe",
                    "args": self.topics
                }

            await websocket.send(json.dumps(subscribe_message))
            print(f"subscribed channels: {self.topics}")
            while True:
                response = await websocket.recv()  # Получаем данные
                
                if is_hidden == True:
                    if isinstance(response, str):
                        await queue.put(response)
                        # print("Received (string):", response)
                    elif isinstance(response, bytes):
                        # Если это байты — разжимаем gzip
                        decompressed_data = gzip.decompress(response)
                        decoded_text = decompressed_data.decode("utf-8")
                        json_data = json.loads(decoded_text)
                        await queue.put(json_data)
                    
                else:
                    await queue.put(json.loads(response))

        pass
    
    async def resubscribe(self):
        pass
        
    
