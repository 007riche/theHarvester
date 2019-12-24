from theHarvester.lib.core import *
import aiohttp


class SearchCertspoter:

    def __init__(self, word):
        self.word = word
        self.totalhosts = set()

    async def do_search(self) -> None:
        base_url = f'https://api.certspotter.com/v1/issuances?domain={self.word}&expand=dns_names'
        headers = {'User-Agent': Core.get_user_agent()}
        try:
            client = aiohttp.ClientSession(headers=headers, timeout=aiohttp.ClientTimeout(total=30))
            response = await async_fetcher.fetch(client, base_url, json=True)
            await client.close()
            if isinstance(response, list):
                for dct in response:
                    for key, value in dct.items():
                        if key == 'dns_names':
                            self.totalhosts.update({name for name in value if name})
            elif isinstance(response, dict):
                self.totalhosts.update({response['dns_names'] if 'dns_names' in response.keys() else ''})
            else:
                self.totalhosts.update({''})
        except Exception as e:
            print(e)

    async def get_hostnames(self) -> set:
        return self.totalhosts

    async def process(self):
        await self.do_search()
        print('\tSearching results.')
