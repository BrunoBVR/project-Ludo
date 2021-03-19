# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class LudoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    position = scrapy.Field()
    title = scrapy.Field()
    year = scrapy.Field()
    notas = scrapy.Field()
    notaRank = scrapy.Field()
    media = scrapy.Field()
    age = scrapy.Field()
    timeOfPlay = scrapy.Field()
    numOfPlayers = scrapy.Field()
    designer = scrapy.Field()
    artist = scrapy.Field()
    dominio = scrapy.Field()
    mecanicas = scrapy.Field()
    imagem = scrapy.Field()
