import mysql.connector
from itemadapter import ItemAdapter

class MySQLPipeline:
    #     def process_item(self, item, spider):
#         return item
    
    def __init__(self):
        self.conn = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            database = 'db-ta-cp',
        )

        self.cur = self.conn.cursor()

        self.cur.execute("""
                         create table if not exists laptop(
                         id bigint(20) not null auto_increment,
                         name varchar(100) not null,
                         cpu varchar(100) not null,
                         gpu varchar(100) not null,
                         storage int(11) not null,
                         ram int(11) not null,
                         display float not null,
                         price int not null,
                         created_at datetime default current_timestamp,
                         updated_at datetime default current_timestamp on update current_timestamp,
                         PRIMARY KEY (id)
                         )""")
    
    def process_item(self, item, spider):
        self.cur.execute("SELECT * FROM laptop where name = %s", (item['name'],))
        result = self.cur.fetchone()

        if result:
            spider.logger.warn("Laptop already in database: %s" % item['name'])

        else:
            self.cur.execute(""" INSERT INTO laptop (name, cpu, gpu, storage, ram, display, price) VALUES (%s, %s, %s, %s, %s, %s, %s) """,
                             (item['name'],
                              item['cpu'],
                              item['gpu'],
                              item['storage'],
                              item['ram'],
                              item['display'],
                              item['price']
                              ))

            self.conn.commit()

        return item
    
    def close_spider(self, spider):
        self.cur.close()
        self.conn.close()

    pass