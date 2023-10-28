import scrapy
from scrapy_splash import SplashRequest 
import pandas as pd #To make a Dataframe -> Might switch this to json based on size?

# This spider starts by first recieving all the detail numbers so 

class TradingeconSpider(scrapy.Spider):
    name = "tradingecon"
    all_data = []

    def start_requests(self):
        urls = ["https://www.forexfactory.com/calendar?week=oct15.2023", 
                "https://www.forexfactory.com/calendar?week=oct22.2023", 
                "https://www.forexfactory.com/calendar?week=oct29.2023"]

        for url in urls:
            yield SplashRequest(       ## Works by leveraging Docker and WSL to create a render of a website using the JS and HTMS
                url,                   ## The specific utl that we want to do this for
                callback=self.parse,   ## Calling the parsing function
                endpoint='render.json',## The render.json endpoint returns the rendered webpage in JSON format
                args={
                    'html': 1, 
                    'png': 1, 
                    'width': 1000, 
                })

    def parse(self, response):
        table_rows = response.xpath('//*[@id="content"]/section[2]/div[3]//table//tbody//tr')
        date = "somedate"
        data = []
        for row in table_rows[1:]:
            if len(row.xpath("./td")) == 1:
                date = row.xpath("./td/span/text()").extract_first()
            if len(row.xpath('./td')) == 11: # making sure the row has 11 cells
                data_event_id = row.xpath('@data-event-id').get()
                date_temp = row.xpath('td[@class="calendar__cell calendar__date"]/text()').get()
                if date_temp:
                    date = date_temp.strip()
                time = row.xpath('td[@class="calendar__cell calendar__time"]/text()').get()
                event = row.xpath('td[contains(@class, "calendar__event")]/div/span[@class="calendar__event-title"]/text()').get()
                currency = row.xpath('td[@class="calendar__cell calendar__currency"]/text()').get()
                impact = row.xpath('td[@class="calendar__cell calendar__impact"]/span/@class').get()[-3:] if row.xpath('td[@class="calendar__cell calendar__impact"]/span/@class').get() else None
                actual = row.xpath('td[contains(@class, "calendar__actual")]/span/text()').get()
                forecast = row.xpath('td[contains(@class, "calendar__forecast")]/span/text()').get()
                previous = row.xpath('td[contains(@class, "calendar__previous")]/span/text()').get()
                
                # Appending data to the list
                data.append({
                    'data_event_id': data_event_id,
                    'date': date,
                    'time': time,
                    'event': event,
                    'currency': currency,
                    'impact': impact,
                    'actual': actual,
                    'forecast': forecast,
                    'previous': previous
                })
        self.all_data.extend(data)

        # After the loop, you can either yield the data directly
        for item in data:
            yield item

    def closed(self, reason):
        # This function is called when the spider closes
        # You can save the data to a DataFrame here if you choose
        df = pd.DataFrame(self.all_data)
        df.to_csv('output.csv', index=False)
        

        




                


                

## The data is of the following type:
## There are 3 types of Rows
    





