# -*- coding: utf-8 -*-
import scrapy
from humle.countrysettings import countries
from humle.items import ScrapedProduct, ScrapedCategory, ScrapedProductCategoryAssociation
from hashlib import sha1

class HumlespiderSpider(scrapy.Spider):
    name = 'humlespider'

    def parse(self, response):
        pass

    def start_requests(self):
        return [scrapy.Request(
            url=x['url'],
            callback=self.parsemainpage,
            cb_kwargs={
                "countryinfo": x,
            }
        ) for x in countries]

    def parsemainpage(self, response, countryinfo: dict):

        topmenuitems = response.xpath('//div[@class="navbar-bg mainmenu_font_size"]/ul/li')[:5]

        for menuitem in topmenuitems:
            maincat = ScrapedCategory()
            maincat['name'] = menuitem.xpath('a/text()').get()
            maincat['url'] = response.urljoin(menuitem.xpath('a/@href').get())
            maincat['platformcategoryid'] = self.createidfromstring(maincat['url'])
            maincat['level'] = 1
            maincat['agegroup'] = "adult"
            maincat['targetgender'] = "unisex"
            maincat['storeid'] = countryinfo['storeid']

            yield maincat

            yield scrapy.Request(
                url=maincat['url'],
                callback=self.parseprodspage,
                cb_kwargs={
                    "countryinfo": countryinfo,
                    "maincat": maincat,
                    "subcat": None,
                    "subsubcat": None
                }
            )

            for subitem in menuitem.xpath('ul/li'):
                subcat = ScrapedCategory()
                subcat['name'] = subitem.xpath('a/text()').get()
                if subcat['name']  == 'Vad har din hud för behov?':
                    subcat['name'] = "Kräm för din hud"
                subcat['url'] = response.urljoin(subitem.xpath('a/@href').get())
                subcat['platformcategoryid'] = self.createidfromstring(subcat['url'])
                subcat['level'] = 2
                subcat['storeid'] = countryinfo['storeid']
                subcat['agegroup'] = "adult"
                subcat['targetgender'] = "unisex"

                yield subcat

                yield scrapy.Request(
                    url=subcat['url'],
                    callback=self.parseprodspage,
                    cb_kwargs={
                        "countryinfo": countryinfo,
                        "maincat": maincat,
                        "subcat": subcat,
                        "subsubcat": None
                    }
                )

                for subs in subitem.xpath('ul/li'):
                    subsubcat = ScrapedCategory()
                    subsubcat['name'] = subs.xpath('a/text()').get()
                    subsubcat['url'] = response.urljoin(subs.xpath('a/@href').get())
                    subsubcat['platformcategoryid'] = self.createidfromstring(subsubcat['url'])
                    subsubcat['level'] = 3
                    subsubcat['storeid'] = countryinfo['storeid']
                    subsubcat['agegroup'] = "adult"
                    subsubcat['targetgender'] = "unisex"

                    yield subsubcat

                    yield scrapy.Request(
                        url=subsubcat['url'],
                        callback=self.parseprodspage,
                        cb_kwargs={
                            "countryinfo": countryinfo,
                            "maincat": maincat,
                            "subcat": subcat,
                            "subsubcat": subsubcat
                        }
                    )

    def parseprodspage(self, response: scrapy.http.Response,
                       countryinfo: dict, maincat: ScrapedCategory,
                       subcat: ScrapedCategory, subsubcat: ScrapedCategory):

        allprods = response.xpath('//div[@class="col-md-3 col-6 product"]')

        for prod in allprods:
            yield scrapy.Request(
                url=response.urljoin(prod.xpath('div/div/a/@href').get()),
                callback=self.parseprod,
                cb_kwargs={
                    "countryinfo": countryinfo,
                    "maincat": maincat,
                    "subcat": subcat,
                    "subsubcat": subsubcat
                }
            )

    def parseprod(self, response: scrapy.http.Response, countryinfo: dict,
                  maincat: ScrapedCategory, subcat: ScrapedCategory, subsubcat: ScrapedCategory):

        oneprod = ScrapedProduct()
        oneprod['name'] = response.xpath('//h1[@class="h2"]/text()').get()
        if oneprod['name'] == 'PRESENTKORT':
            return
        oneprod['url'] = response.url
        oneprod['platformproductid'] = self.createidfromstring(oneprod['url'])
        oneprod['platformvariantid'] = "1"
        oneprod['imageLink'] = response.xpath('//meta[@property="og:image"]/@content').get()
        oneprod['additionalImageLinks'] = []
        oneprod['description'] = response.xpath('//div[@itemprop="description"]/@content').get()
        oldprice = response.xpath('//s[@class="qs-product-before-price product-before-price"]/text()').get()
        if not oldprice:
            oneprod['saleprice'] = None
            oneprod['price'] = response.xpath('//li[@class="list-inline-item h4 font-weight-light mb-0 product-price qs-product-price w-100"]/text()').get().strip().replace(" ","").replace("kr","")
        else:
            oneprod['price'] = response.xpath('//s[@class="qs-product-before-price product-before-price"]/text()').get().strip().replace(" ","").replace("kr","")
            oneprod['saleprice'] = response.xpath('//li[@class="list-inline-item h4 font-weight-light mb-0 product-price qs-product-price w-100"]/text()').get().strip().replace(" ","").replace("kr","")
        if oneprod['price'] is None:
            return
        oneprod['brand'] = "Humle"
        oneprod['gender'] = "unisex"
        oneprod['agegroup'] = "adult"
        oneprod['gtin'] = [None]
        oneprod['color'] = ""
        oneprod['material'] = ""
        oneprod['sizes'] = [None]
        oneprod['instock'] = True
        oneprod['platformcategoryid'] = maincat['platformcategoryid']
        oneprod['additionalcategoryids'] = []
        oneprod['storeid'] = countryinfo['storeid']
        oneprod['mpn'] = ""
        oneprod['platformvariantid'] = ""

        yield oneprod

    @staticmethod
    def createidfromstring(string: str) -> str:
        sha = sha1()
        sha.update(string.encode('utf-8'))
        return sha.hexdigest()[-15:]