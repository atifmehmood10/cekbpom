# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


class CompanieshouseItem(scrapy.Item):
    # define the fields for your item here like:
    Nomor_Registrasi = Field()
    Tanggal_Terbit = Field()
    Diterbitkan_Oleh = Field()
    Produk = Field()
    Nama_Produk = Field()
    Merk = Field()
    Kemasan = Field()
    Pendaftar = Field()
    Penerima_Kontrak = Field()
    pass
