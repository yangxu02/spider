# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html

class AppinfoPipeline(object):
    def process_item(self, item, spider):
        if item['category']:
            item['category'] = item['category'].split("/")[-1]
            item['category'] = item['category'].split("_")[0]
        if item['price']:
            # parsing currency from price
            if item['price'][0].isdigit():
                item['currency'] = '$'
            else:
                item['currency'] = item['price'][0]
                item['price'] = item['price'][1:]
            if item['downloads']:
                downloads = item['downloads'].split(' ')
                item['minDownloads'] = int(downloads[0].replace(',', ''))
                item['maxDownloads'] = int(downloads[-1].replace(',', ''))


        return item

