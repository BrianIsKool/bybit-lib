import asyncio
import aiohttp



class https_utils:
    def __init__(self, istestnet=False):
        self.URL = "api.bybit.com/v5/" if istestnet else "api-testnet.bybit.com/v5/"
        pass
    
    async def https_request(self, path, params):
        full_url = f"https://{self.URL}{path}"
        query_string = aiohttp.helpers.URL(full_url).with_query(params)
        async with aiohttp.ClientSession() as session:
            print(f"Запрос: GET {query_string}")
            async with session.get(full_url, params=params) as resp:
                print(await resp.text())
                return await resp.text()
        


# async def main():
#     client = https_utils(istestnet=True)
#     await client.https_request("market/kline", {
#         "category": "spot",
#         "symbol": "BTCUSDT",
#         "interval": "M",
#         "start": "1525125600000",
#         "end": "1625125900000",
#         "limit": "1000"
#     })

# asyncio.run(main())