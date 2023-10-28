import scrapy
from scrapy import Request

class MydomainSpider(scrapy.Spider):
    name = 'forexfactory'
    allowed_domains = ['forexfactory.com']
    start_urls = ['https://www.forexfactory.com/calendar']


    def parse(self, response):
        for event in response.css('tr.calendar_row'):
            yield {
                'time': event.css('.calendar__time::text').get(),
                'currency': event.css('.calendar__currency::text').get(),
                'impact': event.css('.impact span::attr(title)').get(),
                'event': event.css('.calendar__event::text').get(),
                'detail': event.css('.calendar__event::attr(title)').get(),
                'actual': event.css('.calendar__actual::text').get(),
                'forecast': event.css('.calendar__forecast::text').get(),
                'previous': event.css('.calendar__previous::text').get()}
        