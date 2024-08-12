import scrapy
import math
import re

class PostSpider(scrapy.Spider):
    name = 'post'
    start_urls = [
        "https://www.gadgetsnow.com/laptops/filters/brand=Acer%7CAsus%7CHP%7CLenovo%7CMSI%7CApple%7CDell"
        # "https://www.gadgetsnow.com/laptops/Apple"
        # "https://www.gadgetsnow.com/laptops/Acer"
    ]

    def parse(self, response):
        for post in response.css('div.xWtEW'):
            item = LaptopItem()
            
            # nama 
            name = post.css('.gjwz2::text').get()
            item['name'] = name.split(" Laptop")[0]

            # harga
            temp_price = post.css('.W4x4B::text').get()
            if(temp_price is None):
                item['price'] = 30000000

            elif(',' in temp_price):
                price = temp_price.replace(',', '')
                item['price'] = math.ceil(int(price) * 188)

            # storage
            storage = post.css('.Ja2sG::text')[0].get()
            if 'TB' in storage and '+' not in storage:
                storage_numeric = ''.join(c for c in storage if c.isdigit())
                item['storage'] = int(storage_numeric) * 1024
                # print('TB dan tidak ada +')
                # print(f"tb and not +(plus) {storage}")

            elif 'GB' in storage and '+' not in storage:
                storage_numeric = ''.join(c for c in storage if c.isdigit())
                item['storage'] = int(storage_numeric)
                # print(f'tb {storage}')
                # print(f'GB and not (plus)+ {storage}')

            elif 'GB' in storage and '+' in storage:
                if 'TB' in storage:
                    splits = storage.split('+')
                    for splt in splits:
                        splt = splt.strip()

                        match = re.search(r'(\d+)(GB|TB)', splt)
                        if match:
                            number_found = int(match.group(1))
                            storage_type = match.group(2)

                            if storage_type == 'GB':
                                gb = number_found
                            
                            elif storage_type == 'TB':
                                tb = number_found * 1024
                    
                    item['storage'] = gb + tb
                    # stg = item['storage']
                    # print(f'{storage} = {stg}')
                
                elif 'TB' not in storage:
                    splits = storage.split('+')
                    left = splits[0].strip()
                    right = splits[1].strip()

                    split_word = 'GB'
                    left = int(re.split(split_word,  left)[0])
                    right = int(re.split(split_word,  right)[0])

                    item['storage'] = left + right
                    stg = item['storage']
                    # print(f'{storage} = {stg}'
            else:
                item['storage'] = 1024

            # display
            display = post.css('.Ja2sG::text')[1].get()
            display_numeric = ''.join(c for c in display if c.isdigit() or c == '.')
            item['display'] = float(display_numeric)

            # cpu
            item['cpu'] = post.css('.Ja2sG::text')[2].get()
            # item['gpu'] = post.css('.Ja2sG::text')[3].get()

            # gpu
            if "Apple" in item['name']:
                item['gpu'] = item['cpu']

                if "HN/A" in item['name']:    
                    ram = name.split('/')[2].strip()
                    ram_numeric = ''.join(c for c in ram if c.isdigit())
                    item['ram'] = int(ram_numeric)
                else:
                    ram = name.split('/')[1].strip()
                    ram_numeric = ''.join(c for c in ram if c.isdigit())
                    item['ram'] = int(ram_numeric)
                
                # item['gpu'] = item['cpu']
                # ram = name.split('/')[2].strip()
                # ram_numeric = ''.join(c for c in ram if c.isdigit())
                # item['ram'] = int(ram_numeric)

            else:
                item['gpu'] = post.css('.Ja2sG::text')[3].get()
                ram = name.split('/')[1].strip()
                ram_numeric = ''.join(c for c in ram if c.isdigit())
                item['ram'] = int(ram_numeric)

            data_item = {
                'name' : item['name'],
                'price' : item['price'],
                'storage' : item['storage'],
                'display' : item['display'],
                'cpu' : item['cpu'],
                'gpu' : item['gpu'],
                'ram' : item['ram'],
            }

            # self.data.append(data_item)
            yield data_item

            next_page = response.css('.aldLi a::attr(href)').get()
            if next_page is not None:
                next_page = response.urljoin(next_page)
                yield scrapy.Request(next_page, callback=self.parse)


class LaptopItem(scrapy.Item):
    name = scrapy.Field()
    cpu = scrapy.Field()
    gpu = scrapy.Field()
    storage = scrapy.Field()
    ram = scrapy.Field()
    display = scrapy.Field()
    price = scrapy.Field()

    pass