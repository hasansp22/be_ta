import mysql.connector
from itemadapter import ItemAdapter

# class ScrapePipeline:
#     def process_item(self, item, spider):
#         return item

class MySQLPipeline:
    def __init__(self, mysql_uri, mysql_db):
        self.mysql_uri = mysql_uri
        self.mysql_db = mysql_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mysql_uri=crawler.settings.get('MYSQL_URI'),
            mysql_db=crawler.settings.get('MYSQL_DB')
        )

    def open_spider(self, spider):
        self.conn = mysql.connector.connect(database=self.mysql_db)
        self.cursor = self.conn.cursor()

    def close_spider(self, spider):
        self.conn.close()

    def process_item(self, item, spider):
        # Sesuaikan query MySQL dan tabel
        query = "INSERT INTO laptop (name, cpu, gpu, storage, ram, display, price) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        values = (item['name'], item['cpu'], item['gpu'], item['storage'], item['ram'], item['display'], item['price'])

        self.cursor.execute(query, values)
        self.conn.commit()

        return item
    pass