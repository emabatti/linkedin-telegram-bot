from bs4 import BeautifulSoup
from requests_html import HTMLSession
import config
import asyncio
import telegram
import time

class Job:
    title: str
    company: str
    time_ago: str
    link: str


async def main():
    bot = telegram.Bot(config.api_token) 
    session = HTMLSession()
     
    async def send_message(job: Job = Job()):
        text = f'<b><a href="{job.link}">{job.title}</a></b>'
        await bot.send_message(text=text, chat_id=config.chat_id, parse_mode="HTML")
    
    # preparing driver to allow for js loading before parsing the page
    while True:
        jobs = []
        for url in config.urls:
            page = session.get(url)
            soup = BeautifulSoup(page.text,"lxml")

            listings = soup.select('#main-content section > ul li')

            if listings:
                for listing in listings:
                    job = Job()
                    job.title = listing.h3.string.strip()
                    job.company = listing.h4.a.string.strip()
                    job.time_ago = listing.time.string.strip()
                    job.link = listing.a['href'].strip()
                    jobs.append(job)
                
        for job in jobs:
            await send_message(job)
        time.sleep(config.seconds)

if __name__=="__main__":
    asyncio.run(main())
