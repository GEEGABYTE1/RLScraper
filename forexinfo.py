import scrapy
from scrapy_splash import SplashRequest
import pandas as pd
import numpy as np
import base64

lua_script = """
function main(splash, args)
  splash:go(args.url)
  splash:wait(0.1)

  local element = splash:select('.calendar__detail-link')
  element:mouse_click()
    

  return {
    html = splash:html(),
    png = splash:png(),  -- Capture the screenshot
  }
end
"""

class ForexinfoSpider(scrapy.Spider):
    name = "forexinfo"

## This spider has to do the following. Based on the URLs that the script gives us, it has to find the detail 
## From this detail it has has to be able to scrape the relevant information for the detail. It can be a new dataframe
# as long as the detail number is found and stored  properly
#  

    def start_requests(self):
        url = 'https://www.forexfactory.com/calendar?week=oct15.2023'
        yield SplashRequest(
            url, 
            self.parse, 
            endpoint='execute',
            args={
                'lua_source': lua_script,  # the Lua script with splash:png()
                'wait': 0.1 # Time to wait for the page to load
            }
        )

    def parse(self, response):
        # Save the screenshot
        with open('screenshot.png', 'wb') as f:
            f.write(response.data['png'])