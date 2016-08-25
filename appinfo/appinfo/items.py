# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class AppinfoItem(Item):
    # app id
    appId = Field()
    # app name
    name = Field()
    # app developer(individual or company)
    developer = Field()
    # top category: game ...
    category = Field()
    # sub category: card ...
    subCategory = Field()
    # app price
    price = Field()
    # app price currency
    currency = Field()
    # in app msg
    inAppMsg = Field()
    # star count / review count
    star = Field()
    # star rate in 5 stars / start in review
    starInFive = Field()
    # g+ recommends
    gPlusRecommends = Field()
    # app desc
    desc = Field()
    # app meta
    updated = Field()
    fileSize = Field()
    downloads = Field()
    minDownloads = Field()
    maxDownloads = Field()
    version = Field()
    osRequired = Field()
    contentRating = Field()
    # app recommends
    similarApps = Field()
    otherApps = Field()
