import scrapy
from scrapy_splash import SplashRequest

class AdamchoiSpider(scrapy.Spider):
    name = "adamchoi"
    allowed_domains = ["www.adamchoi.co.uk", "0.0.0.0", "localhost"]
    # start_urls = ["https://www.adamchoi.co.uk"]
    
    script = '''
        function main(splash, args)
            splash.private_mode_enabled = false
            assert(splash:go(args.url))
            assert(splash:wait(2))
            all_matches = assert(splash:select_all("label.btn.btn-sm.btn-primary"))
            all_matches[2]:mouse_click()
            assert(splash:wait(3))
            splash:set_viewport_full()
            return {splash:png(), splash:html()}
        end
    '''
    
    def start_requests(self):
        yield SplashRequest(url='https://www.adamchoi.co.uk/overs/detailed', callback=self.parse, endpoint="render.html", args={"wait": 3})

    def parse(self, response):
        rows = response.xpath('//tr')[1:20]
        
        for row in rows:
            date = row.xpath('./td[1]/text()').get()
            home_team = row.xpath('./td[2]/text()').get()
            score = row.xpath('./td[3]/text()').get()
            away_team = row.xpath('./td[4]/text()').get()
            yield{
                'date': date,
                'home_team': home_team,
                'score': score,
                'away_team': away_team
            }

# docker ---> docker run -it -p 8050:8050 scrapinghub/splash
# To run ---> scrapy crawl adamchoi -o football_data.json