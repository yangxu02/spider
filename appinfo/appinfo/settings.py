# Scrapy settings for appinfo project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'appinfo'
BOT_VERSION = '1.0'

SPIDER_MODULES = ['appinfo.spiders']
NEWSPIDER_MODULE = 'appinfo.spiders'
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)

ITEM_PIPELINES = {
    'appinfo.pipelines.AppinfoPipeline':100
}

FEED_EXPORTERS = {
    'csv': 'appinfo.exporters.AppinfoCsvExporter'
}

EXPORT_FIELDS = [
    'appId',
    'name',
    'developer',
    'category',
    'subCategory',
    'price',
    'currency',
    'inAppMsg',
    'star',
    'starInFive',
    'gPlusRecommends',
    'desc',
    'updated',
    'fileSize',
    'downloads',
    'minDownloads',
    'maxDownloads',
    'version',
    'osRequired',
    'contentRating',
    'similarApps',
    'otherApps'
]

EXPORT_CSV_DELIMITER = '|'
