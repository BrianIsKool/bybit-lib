from bybit_python.websocket_streams import websocket_streams
from bybit_python.https_requests import https_requests
import asyncio
import time



class bybit:
    def __init__(self, queue, api_key="", api_secret="", testnet=False, market="spot"):
        """_summary_

        Args:
            queue (_type_): asyncio.Queue().
            api_key (str, optional): _description_. Defaults to "".
            api_secret (str, optional): _description_. Defaults to "".
            testnet (bool, optional): _description_. Defaults to False.
            market (str, optional): _description_. Defaults to "spot", can be "linear", "inverse", "option".
        """
        self.api_secret = api_secret
        self.api_key = api_key
        self.queue = queue  
        self.expires = int((time.time() + 1) * 1000)
        self.URL = "bybit.com/v5"
        self.websocket = websocket_streams(url=self.URL, market=market)
        self.https = https_requests()

        
    
    # async def authorize(self):
    #     self.ws.ws_send(json.dumps({
    #                             "op": "auth",
    #                             "args": [self.api_key, self.expires, self.generate_signature()]
    #                         })
    #                     )

    async def subscribe(self):
        if self.websocket.utils.topics != []:
            subscribe_task = asyncio.create_task(self.websocket.utils.subscribe(self.queue))
        else:
            print('nothing in topics!')
        
        if self.websocket.utils.hidden_topics != []:
            subscribe_hidden_api_task = asyncio.create_task(self.websocket.utils.subscribe(queue=self.queue, is_hidden=True))
        else:
            print("nothing in hidden_topics!")

    # async def generate_signature(self):
    #     return str(hmac.new(
    #             bytes(self.api_secret, "utf-8"),
    #             bytes(f"GET/realtime{self.expires}", "utf-8"), digestmod="sha256"
    #             ).hexdigest())
    #     pass