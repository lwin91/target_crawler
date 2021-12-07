# -*- coding: utf-8 -*-
import scrapy
import json

class TargetSpider(scrapy.Spider):
    name = 'target'
    allowed_domains = ['target.com']

    def __init__(self, url=None, *args, **kwargs):
        super(TargetSpider, self).__init__(*args, **kwargs)
        self.start_urls = [url,]

    def parse(self, response):
        item = {}

        item['url'] = response.url 
        item['tcin'] = response.xpath('//div[b/text()="TCIN"]/text()').extract()[-1]
        item['upc'] = response.xpath('//div[b/text()="UPC"]/text()').extract()[-1]
        item['price'] = response.xpath('//div[@data-test="product-price"]/text()').extract_first()
        item['currency'] = response.xpath('//div[@data-test="product-price"]/text()').extract_first()
        item['title'] = response.xpath('//h1[@itemprop="name"]/span/text()').extract_first()
        item['description'] = response.xpath('//h3[text()="Description"]/following-sibling::div/text()').extract_first()
        item['specs'] = response.xpath('//h3[text()="Specifications"]/following-sibling::div/div/text()').extract_first() 
        item['ingredients'] = response.xpath('//script/text()').re('"ingredients":"[\w\ \,\-\)\(\:\.\/\\\]+')[0]
        
        api_key = response.xpath('//script/text()').re('"x-api-key","value":"[\w]+')[0].split('"')[-1]
        pricing_store_id = response.xpath('//script/text()').re('"pricing_store_id":"[\d]+')[0].split('"')[-1]
        url = 'https://redsky.target.com/redsky_aggregations/v1/web/pdp_client_v1?key={}&tcin={}&pricing_store_id={}'.format(api_key, response.xpath('//div[b/text()="TCIN"]/text()').extract()[-1], pricing_store_id)
        request = scrapy.Request(url, callback=self.parse_first)
        request.meta['item'] = item 
        yield request
    
    def parse_first(self, response):
        item = response.meta['item']
        j = json.loads(response.text)
        item['price'] = j['data']['product']['price']['current_retail']
        currency = j['data']['product']['price']['formatted_current_price']
        if '$' in currency:
            item['currency'] = 'USD'
        else:
            item['currency'] = currency
        yield item

