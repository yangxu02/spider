# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html

from scrapy.conf import settings
from scrapy.contrib.exporter import CsvItemExporter

class AppinfoCsvExporter(CsvItemExporter):
    def __init__(self, *args, **kwargs):
        kwargs['delimiter'] = settings.get('EXPORT_CSV_DELIMITER', '\001')
        kwargs['fields_to_export'] = settings.getlist('EXPORT_FIELDS') or None
        kwargs['encoding'] = settings.getlist('EXPORT_ENCODING', 'utf-8')
        super(AppinfoCsvExporter, self).__init__(*args, **kwargs)
        self.include_headers_line = settings.getbool('export_csv_headers', true);



