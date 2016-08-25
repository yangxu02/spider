__author__ = 'ulyx'

import string
import scrapy
from scrapy.http import Request
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from appinfo.items import AppinfoItem

class Parser:
    def __init__(self):
        pass

    @staticmethod
    def parse_array_and_concat(array, tag):
        i = len(array) - 1
        res = ""
        while i >= 0:
            value = array[i]
            # print tag, '@', i, value.encode('utf-8')
            i -= 1
            value = string.strip(value, '. -"*')
            if value:
                res = value + ';' + res
        return res

    @staticmethod
    def parse_desc_item(tags, hxs, item):
        for tag, xpath in tags.iteritems():
            values = hxs.select(xpath).extract()
            item[tag] = ""
            if len(values) > 0:
                selector = HtmlXPathSelector(text=values.pop())
                intros = selector.select('//text()').extract()
                item[tag] = item[tag] + Parser.parse_array_and_concat(intros, 'intro')
                # paragraphs = selector.select('//p/text()').extract()
                # item[tag] = item[tag] + self.parse_array_and_concat(paragraphs, 'para')
                print tag, '=', item[tag].encode('utf-8')

    @staticmethod
    def parse_base_item(tags, hxs, item):
        for tag, xpath in tags.iteritems():
            values = hxs.select(xpath).extract()
            if len(values) != 0:
                item[tag] = string.strip(values.pop(), ' -"')
            else:
                item[tag] = ""
            print tag, '=', item[tag].encode('utf-8')

    @staticmethod
    def parse_app_recommends(recommends, hxs, item):
        selectors = hxs.select(recommends['xpath']['top'])
        # print selectors.extract()
        for cluster in selectors:
            selector = HtmlXPathSelector(text=cluster.extract())
            headings = selector.select(recommends['xpath']['heading']).extract()
            field = recommends['tag']['more']
            if len(headings) != 0:
                heading = string.lower(string.strip(headings.pop()))
                if heading == 'similar':
                    field = recommends['tag']['similar']
            item[field] = selector.select(recommends['xpath']['apps']).extract()
            print field, '=', item[field]

    @staticmethod
    def parse_gplus_recommend(response):
        item = response.meta['item']
        gplus = response.meta['gplus']
        hxs = HtmlXPathSelector(response)
        values = hxs.select(gplus['xpath']['value']).extract()
        if len(values) != 0:
            value = string.strip(values.pop())
            value = string.split(value, " ")[0]
            value = string.lstrip(value, '+')
            item[gplus['tag']] = value
        return item

    @staticmethod
    def parse_gplus_link(gplus, hxs, item):
        url = hxs.select(gplus['xpath']['url']).extract()
        yield Request(url, callback=Parser.parse_gplus_recommend, meta={'item':item, 'gplus':gplus})


class AppinfoSpider(BaseSpider):
    name = "appinfo"
    allowed_domains = ["play.google.com"]
    base_url = 'https://play.google.com/store/apps/details?id='
    start_urls = [
        "https://play.google.com/store/apps/details?id=com.rovio.angrybirdsrio"
    ]

    baseTags = dict({
        'name': '//div[@class="document-title"]/div/text()',
        'developer': '//div[@itemprop="author"]/a/span[@itemprop="name"]/text()',
        'updated': '//div[@itemprop="author"]/div[@class="document-subtitle"]/text()',
        'category': '//a[@class="document-subtitle category"]/@href',
        'subCategory': '//a[@class="document-subtitle category"]/span[@itemprop="genre"]/text()',
        'price': '//span[@itemprop="offers"]/meta[@itemprop="price"]/@content',
        'inAppMsg': '//div[@class="inapp-msg"]/text()',
        'star': '//meta[@itemprop="ratingCount"]/@content',
        'starInFive': '//meta[@itemprop="ratingValue"]/@content',
        #'gPlusRecommends': '//div[@id="___plusone_1"]/iframe/@src',
        ## may be very long
        'desc': '//div[@class="id-app-orig-desc"]/text()',
        #'appMeta': '//div[@class="meta-info"]',
        'updated': '//div[@class="meta-info"]/div[@itemprop="datePublished"]/text()',
        'fileSize': '//div[@class="meta-info"]/div[@itemprop="fileSize"]/text()',
        'downloads': '//div[@class="meta-info"]/div[@itemprop="numDownloads"]/text()',
        'version': '//div[@class="meta-info"]/div[@itemprop="softwareVersion"]/text()',
        'osRequired': '//div[@class="meta-info"]/div[@itemprop="operatingSystems"]/text()',
        'contentRating': '//div[@class="meta-info"]/div[@itemprop="contentRating"]/text()',
        #'appRecommends':'//div[@class="details-section recommendation"]/div/div'
    })

    descTag = dict({
        'desc': '//div[@class="id-app-orig-desc"]'
    })

    appRecommends = {
        'xpath': {
            'top': '//div[@class="details-section recommendation"]/div/div',
            'heading': '//h1[@class="heading"]/text()',
            'apps': '//div[@class="card no-rationale square-cover apps small"]/@data-docid'
        },
        'tag': {
            'similar': 'similarApps',
            'more': 'otherApps',
        }
    }

    gPlusRecommend = {
        'xpath': {
            'url' : '//div[@id="___plusone_1"]/iframe/@src',
            'value' : '//span[@class="A8 eja"]'
        },
        'tag': 'gPlusRecommends'
    }

    parsers = [
        {'parser': Parser.parse_base_item, 'tags': baseTags},
        {'parser': Parser.parse_desc_item, 'tags': descTag},
        {'parser': Parser.parse_app_recommends, 'tags': appRecommends},
    ]

    def __init__(self, filename=None):
        if filename:
            with open(filename, 'r') as f:
                self.start_urls = [self.base_url + appid.strip() for appid in f.readlines()]

    def parse(self, response):

        item = AppinfoItem()
        item['appId'] = response.url.split("=")[-1]
        hxs = HtmlXPathSelector(response)
        for parser in self.parsers:
            parser['parser'](parser['tags'], hxs, item)
        gplus = self.gPlusRecommend
        url = hxs.select(gplus['xpath']['url']).extract()
        if len(url) != 0:
            url = url[0]
            yield Request(url, callback=self.itemParser.parse_gplus_recommend, meta={'item': item, 'gplus': gplus})
        else:
            yield item


