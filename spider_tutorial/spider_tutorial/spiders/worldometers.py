import scrapy


class WorldometersSpider(scrapy.Spider):
    name = "worldometers"
    allowed_domains = ["www.worldometers.info"]
    start_urls = ["https://www.worldometers.info/world-population/population-by-country"]

    def parse(self, response):
        
        # title = response.xpath('//h1/text()').get()
        countries = response.xpath('//td/a')
        
        for country in countries:
            country_name = country.xpath('.//text()').get()
            link = country.xpath('.//@href').get()
            

            # To loop through the countries and their links
            # yield {
            #     'country-name': country_name,
            #     'link': link,
            # }
            
            
            
            # absolute url
            # absolute_url = f'https://www.worldometers.info/{link}'
            # or
            # absolute_url = response.urljoin(link)
            # yield scrapy.Request(url=absolute_url)
            
            
            # relative url
            # yield response.follow(url=link)
            
            
            # scraping dta from multiple links
            yield response.follow(url=link, callback=self.parse_country)
            
    def parse_country(self, response):
        rows = response.xpath("(//table[contains(@class, 'table')])[1]/tbody/tr")
        for row in rows:
            year = row.xpath(".//td[1]/text()").get()
            population = row.xpath(".//td[2]/text()").get()
            
            yield {
                'year': year,
                'population': population,
            }