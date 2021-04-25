import re

import scrapy
from scrapy import Request
from .. items import CompanieshouseItem


class CekbpomSpider(scrapy.Spider):
    name = 'cekbpom'
    allowed_domains = ['cekbpom.pom.go.id']
    start_urls = ['https://cekbpom.pom.go.id/']

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, cookies={'store_language': 'en'}, callback=self.parse)
    # We can have dynamic term as well but for current requirements we can go wtih this
    def parse(self, response):
        url = response.xpath('/html/body/div[2]/div[1]/a/@href').get()
        url = url + "/all/row/10/page/0/order/4/DESC/search/6/mandiri"
        yield Request(url, cookies={'store_language': 'en'}, callback=self.parse_pages)

    # add pagination
    def parse_pages(self, response):
        total_pages = response.xpath('//*[@id="tb_total"]/text()').get()
        current_page = response.url
        if int(total_pages) > 1:
            for i in range(1, 2):
                previous_page = "page/{}".format(i - 1)
                next_page = "page/{}".format(i)
                current_page = current_page.replace(previous_page, next_page)
                yield Request(current_page, cookies={'store_language': 'en'}, callback=self.get_urls)

    def get_urls(self, response):
        home = response.url
        home = home.replace("/all/row/10/page/0/order/4/DESC/search/6/mandiri", "")
        home = home.replace("/all/row/10/page/1/order/4/DESC/search/6/mandiri", "")
        home = home.replace("produk", "detil")
        urls = response.xpath(
            "//*[@class= 'tabelajax']/tr[@title='Klik untuk menampilkan detil data']/@urldetil").extract()
        for row in urls:
            url = str(home) + '/produk' + str(row)
            yield Request(url, cookies={'store_language': 'en'}, callback=self.parse_item)

    def parse_item(self, response):
        product_details = CompanieshouseItem()
        tables = response.xpath("//table")
        for table in tables:
            for row in table.xpath("//*[@class='subs']"):
                key = row.xpath("../td[1]/text()").get()
                value = row.xpath("../td[2]/text()").get()
                if key == 'Nomor Registrasi':
                    product_details['Nomor_Registrasi'] = value
                elif key == 'Tanggal Terbit':
                    product_details['Tanggal_Terbit'] = value
                elif key == 'Diterbitkan Oleh':
                    product_details['Diterbitkan_Oleh'] = value
                elif key == 'Produk':
                    product_details['Produk'] = value
                elif key == 'Nama Produk':
                    product_details['Nama_Produk'] = value
                elif key == 'Merk':
                    product_details['Merk'] = value
                elif key == 'Kemasan':
                    product_details['Kemasan'] = value
                elif key == 'Pendaftar':
                    product_details['Pendaftar'] = value
                elif key == 'Penerima Kontrak':
                    product_details['Penerima_Kontrak'] = value
        yield product_details
