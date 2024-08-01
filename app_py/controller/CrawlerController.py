from app_py import app, db, response
from flask import jsonify, request
import crochet
crochet.setup()
from scrapy import signals
from scrapy.crawler import CrawlerRunner, CrawlerProcess
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor
from scrapy.signalmanager import dispatcher
import time
from sqlalchemy import func

from app_py.scrape.crawl.spiders.post_scrape import PostSpider
import mysql.connector

from app_py.model.LaptopModel import Laptop

output_data = []
crawl_runner = CrawlerRunner()
url = PostSpider.start_urls

@crochet.run_in_reactor
def scrape_with_crochet(url):
    dispatcher.connect(_crawler_result, signal=signals.item_scraped)
    eventual = crawl_runner.crawl(PostSpider, category = url)
    
    return eventual

def _crawler_result(item, response, spider):
    output_data.append(dict(item))

def simpan_crawler():
    conn = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            database = 'db-ta-cp',
        )
    
    global output_data
    global url

    cur = conn.cursor()
    
    table = 'laptop'
    cur.execute('''SELECT count(*) FROM information_schema.tables WHERE table_schema = %s AND table_name = %s''', (conn.database, table))
    
    row_count = cur.fetchone()[0]
    if row_count == 0:
        scrape_with_crochet(url = url)
        # time_sleep(url)
        # time.sleep(180)
        # time.sleep(30)
        time.sleep(10)

        cur.execute("""
                    create table if not exists laptop(
                    id bigint(20) not null auto_increment,
                    name varchar(100) not null,
                    brand varchar(25) not null,
                    cpu varchar(100) not null,
                    gpu varchar(100) not null,
                    storage int(11) not null,
                    ram int(11) not null,
                    display float not null,
                    weight float not null,
                    price int not null,
                    created_at datetime default current_timestamp,
                    updated_at datetime default current_timestamp on update current_timestamp,
                    PRIMARY KEY (id)
                    )""")
        
        for item in output_data:
            def _weight():
                if item["display"] > 11 and item["display"] < 14 and any(word in item["gpu"] for word in ['Intel', 'Integrated']):
                    # print('1')
                    weight_temp = 1.3
                elif item["display"] >= 14 and item["display"] < 16 and any(word in item["gpu"] for word in ['Intel', 'Integrated', 'AMD']):
                    # print('2')
                    weight_temp = 1.5
                elif item["display"] >= 15 and item["display"] < 16 and any(word in item["gpu"] for word in ['AMD', 'RTX']):
                    # print('3')
                    weight_temp = 2.3
                elif item["display"] >= 16 and item["display"] < 17 and any(word in item["gpu"] for word in ['AMD', 'RTX']):
                    # print('3')
                    weight_temp = 2.5
                elif item["display"] >= 17:
                    # print('4')
                    weight_temp = 2.8
                else:
                    # print('5')
                    weight_temp = 2.0

                return weight_temp

            if row_count == 0:
                cur.execute("SELECT COUNT(*) FROM laptop WHERE name = %s", (item['name'],))
                row_count = cur.fetchone()[0]

                brand_name = item["name"].split()[0]
                weight = _weight()

                cur.execute(""" INSERT INTO laptop (name, brand, cpu, gpu, storage, ram, display, weight, price) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) """,
                            (item["name"],
                            brand_name,
                            item["cpu"],
                            item["gpu"],
                            item["storage"],
                            item["ram"],
                            item["display"],
                            weight,
                            item["price"]
                            ))
            
        conn.commit()
        conn.close()

        print("Success")
    else: # The code will come here if it doesn't find the URL data in DB
        scrape_with_crochet(url = url)
        # time_sleep(url)
        time.sleep(180)
        # time.sleep(30)
        # time.sleep(10)

        for item in output_data:
            def _weight():
                if item["display"] > 11 and item["display"] < 14 and any(word in item["gpu"] for word in ['Intel', 'Integrated']):
                    # print('1')
                    weight_temp = 1.3
                elif item["display"] >= 14 and item["display"] < 16 and any(word in item["gpu"] for word in ['Intel', 'Integrated', 'AMD']):
                    # print('2')
                    weight_temp = 1.5
                elif item["display"] >= 15 and item["display"] < 16 and any(word in item["gpu"] for word in ['AMD', 'RTX']):
                    # print('3')
                    weight_temp = 2.3
                elif item["display"] >= 16 and item["display"] < 17 and any(word in item["gpu"] for word in ['AMD', 'RTX']):
                    # print('3')
                    weight_temp = 2.5
                elif item["display"] >= 17:
                    # print('4')
                    weight_temp = 2.8
                else:
                    # print('5')
                    weight_temp = 2.0

                return weight_temp
            
            cur.execute("SELECT COUNT(*) FROM laptop WHERE name = %s", (item['name'],))
            row_count = cur.fetchone()[0]
            
            if row_count == 0:
                brand_name = item["name"].split()[0]
                weight = _weight()

                cur.execute(""" INSERT INTO laptop (name, brand, cpu, gpu, storage, ram, display, weight, price) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) """,
                            (item["name"],
                            brand_name,
                            item["cpu"],
                            item["gpu"],
                            item["storage"],
                            item["ram"],
                            item["display"],
                            weight,
                            item["price"]
                            ))
                
                print('berhasil')
            else:
                print('gagal')
                # return None
                
        conn.commit()
        conn.close()

    return jsonify(output_data)

def display_option():
    try:
        # Mengambil satu data untuk setiap nilai unik dari kolom display yang spesifik
        laptops = db.session.query(Laptop.display, func.MIN(Laptop.id)).filter(Laptop.display.in_([13, 14, 15.6, 16])).group_by(Laptop.display).all()
        # Menggunakan kisaran nilai float untuk mencakup 15.6
        # laptops = db.session.query(Laptop.display, func.MIN(Laptop.id)).filter(Laptop.display >= 15.5, Laptop.display < 15.7).group_by(Laptop.display).all()

        result = []
        for laptop in laptops:
            # Mengambil data lengkap berdasarkan ID yang ditemukan sebelumnya
            laptop_data = Laptop.query.filter_by(id=laptop[1]).first()
            result.append(
                {
                    'id': laptop_data.id,
                    'display': laptop_data.display,
                    # Tambahkan atribut lain yang ingin Anda ambil
                }
            )

        # laptop = Laptop.query.all()
        # laptop = Laptop.query.distinct(Laptop.display).all()
        # result = []
        # for i in laptop:
        #     laptop_data = Laptop.query.filter_by(id=i[1]).first()
        #     result.append(
        #         {
        #             'id': laptop_data.id,
        #             'display': laptop_data.display,
        #         }
        #     )
        return jsonify(result)
    
    except Exception as e:
        print(e)

    # return None