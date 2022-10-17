import scrapy

class ScrapedProduct(scrapy.Item):
    platformproductid = scrapy.Field()
    platformvariantid = scrapy.Field()
    imageLink = scrapy.Field()
    additionalImageLinks = scrapy.Field()
    price = scrapy.Field()
    saleprice = scrapy.Field()
    brand = scrapy.Field()
    name = scrapy.Field()
    gender = scrapy.Field()
    shipping = scrapy.Field()
    shippingWeight = scrapy.Field()
    sizes = scrapy.Field()
    mpn = scrapy.Field()
    gtin = scrapy.Field()
    color = scrapy.Field()
    material = scrapy.Field()
    instock = scrapy.Field()
    description = scrapy.Field()
    url = scrapy.Field()
    platformcategoryid = scrapy.Field()
    additionalcategoryids = scrapy.Field()
    agegroup = scrapy.Field()
    multipack = scrapy.Field()

    storeid = scrapy.Field()

    def __eq__(self, other):
        try:
            return self.identifier == other.identifier
        except (AttributeError, KeyError):
            return False

    def __lt__(self, other):
        try:
            return self.identifier < other.identifier
        except (AttributeError, KeyError):
            return False

    def __hash__(self):
        try:
            return hash(self.identifier)
        except AttributeError:
            return hash(1)

    def __repr__(self):
        return str(self['platformproductid']) + " " + self['name']

    @property
    def identifier(self):
        return self['platformproductid'] + self['platformvariantid']


class ScrapedCategory(scrapy.Item):
    platformcategoryid = scrapy.Field()
    name = scrapy.Field()
    url = scrapy.Field()
    targetgender = scrapy.Field()
    agegroup = scrapy.Field()
    coloroptions = scrapy.Field()
    level = scrapy.Field()
    generatedkeywords = scrapy.Field()

    storeid = scrapy.Field()

    def __eq__(self, other):
        try:
            return self['platformcategoryid'] == other['platformcategoryid']
        except (AttributeError, KeyError):
            return False
        except TypeError:
            return False

    def __lt__(self, other):
        try:
            return self['platformcategoryid'] < other['platformcategoryid']
        except AttributeError:
            return False

    def __hash__(self):
        try:
            return hash(self['platformcategoryid'])
        except AttributeError:
            return hash(1)

    def __repr__(self):
        return self['platformcategoryid'] + " " + self['name']


class ScrapedProductCategoryAssociation(scrapy.Item):
    category = scrapy.Field()
    productid = scrapy.Field()
    storeid = scrapy.Field()