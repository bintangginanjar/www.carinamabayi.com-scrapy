import scrapy
import string

from scrapy.loader import ItemLoader
from nama.items import NamaItem

class NamaSpider(scrapy.Spider):
    name = 'nama'

    custom_settings = {
        'FEED_EXPORT_FIELDS': [
            'nama',
            'jenisKelamin',
            'asalBahasa',
            'kelaminAsal',
            'artiNama'
        ]
    }

    def start_requests(self):		
        charList = list(string.ascii_uppercase)

        baseUrl = 'https://carinamabayi.com/berawalan-'

        for char in charList:
            targetUrl = baseUrl + char + '/'

            prodResponse = scrapy.Request(targetUrl, callback = self.parse)
            prodResponse.meta['dont_cache'] = True

            yield prodResponse

    def parse(self, response):		
		
        for row in response.xpath('//*[@class="table table-striped"]//tbody//tr'):
            loader = ItemLoader(item = NamaItem(), selector = row)
            loader.add_xpath('nama', 'td[2]//text()')
            loader.add_xpath('jenisKelamin', 'td[3]//text()')
            loader.add_xpath('asalBahasa', 'td[4]//text()')
            loader.add_xpath('kelaminAsal', 'td[5]//text()')
            loader.add_xpath('artiNama', 'td[6]//text()')

            #nextPage = response.xpath('//*[@class="pagination pagination-centered"]//ul//li[last()]//a//text()')
            nextPage = response.xpath('//*[@class="pagination pagination-centered"]//ul//li[last()]')

            #if (nextPage.get() == '>'):
            #print(nextPage.xpath('a//text()').get())
            if (nextPage.xpath('a//text()').get() == '>'):
                yield response.follow(nextPage.xpath('a/@href').get(), self.parse)
                #print (nextPage.xpath('a/@href').get())

            yield loader.load_item()