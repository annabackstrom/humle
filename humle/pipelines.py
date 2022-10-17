from humle.items import ScrapedProduct, ScrapedCategory, ScrapedProductCategoryAssociation
from humle.countrysettings import countries
from humle.machineapiconnector import MachineAPIWrapper
from humle.listfinder import bisectleftwithattribute, finditemsinlistwithbisect

class HumlePipeline(object):
    countryproperties: {str: {str: list}} = dict()
    productcount = 0
    duplicatecount = 0

    def process_item(self, item, spider):
        storeid = item['storeid']
        if storeid not in self.countryproperties:
            self.countryproperties[storeid] = {"products": [],
                                               "categories": []}

        if isinstance(item, ScrapedCategory):
            if [x['name'] for x in self.countryproperties[storeid]['categories']].count(item['name']) >= 5:
                return
            self.countryproperties[storeid]['categories'].append(item)
        if isinstance(item, ScrapedProduct):
            self.productcount += 1
            existingproducts = finditemsinlistwithbisect(itemlist=self.countryproperties[storeid]['products'],
                                                         attrname="identifier",
                                                         object=item)
            if len(existingproducts) > 0:
                for existingproduct in existingproducts:
                    self.duplicatecount += 1
                    if item['platformcategoryid'] not in [*existingproduct['additionalcategoryids'],
                                                          existingproduct['platformcategoryid']]:
                        existingproduct['additionalcategoryids'].append(item['platformcategoryid'])
                return item
            index = bisectleftwithattribute(self.countryproperties[storeid]['products'], item, "identifier")
            self.countryproperties[storeid]['products'].insert(index, item)
        if isinstance(item, ScrapedProductCategoryAssociation):
            existingproducts = finditemsinlistwithbisect(itemlist=self.countryproperties[storeid]['products'],
                                                         attrname="platformproductid",
                                                         object=item['productid'])
            if len(existingproducts) > 0:
                for existingproduct in existingproducts:
                    if item['category']['platformcategoryid'] not in [*existingproduct['additionalcategoryids'],
                                                                      existingproduct['platformcategoryid']]:
                        existingproduct['additionalcategoryids'].append(item['category']['platformcategoryid'])
        return item

    def close_spider(self, spider):
        # https://shopifyappdev3.amandaai.com/pridacapi
        # https://sapp.amandaai.com/pridacapi

        wrapper = MachineAPIWrapper(host="https://pridacapi.amandaai.com",
                                    username=spider.settings.attributes.get('FTP_USER').value,
                                    password=spider.settings.attributes.get('FTP_PASSWORD').value)
        for key, value in self.countryproperties.items():
            countryinfo = next(iter([x for x in countries if x['storeid'] == key]), None)
            if countryinfo is None:
                print("Could not find countryinfo for store with id {}".format(key))
                continue
            wrapper.postproductsandcategories(storename=countryinfo['storename'],
                                              storeid=key,
                                              productsandcategories={
                                                  "products": [dict(x) for x in list(set(value['products']))],
                                                  "categories": [dict(x) for x in list(set(value['categories']))]
                                              })
