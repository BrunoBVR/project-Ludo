import scrapy
from ludo.items import LudoItem


class LudoSpider(scrapy.Spider):
    name = 'ludo'

    start_urls = ["https://www.ludopedia.com.br/ranking?pagina=1"]

    n_pages = 1

    # Looping throguh n_pages
    for i in range(2, n_pages+1):
        start_urls.append(f"https://www.ludopedia.com.br/ranking?pagina={i}")

    def parse(self, response):
        item = LudoItem()
        count = 0
        for url in response.xpath("//h4[contains(@class, 'media-heading')]/a//@href").extract():
            url = url+"?v=creditos"
            item['title'] = response.xpath("//h4[contains(@class, 'media-heading')]/a//@title").extract()[count]
            item['position'] = response.xpath("//h4[contains(@class, 'media-heading')]/span//descendant::text()").extract()[count]
            item['year'] = response.xpath("//h4[contains(@class, 'media-heading')]/small/descendant::text()").extract()[count]
            item['notas'] = response.xpath("//div[contains(@class, 'rank-info')]/span/a/b/descendant::text()").extract()[count]
            item['notaRank'] = response.xpath("//div[contains(@class, 'rank-info')]/span/b/descendant::text()").extract()[::3][count]
            item['media'] = response.xpath("//div[contains(@class, 'rank-info')]/span/b/descendant::text()").extract()[1::3][count]

            count+=1
            request = scrapy.Request(url, callback=self.parse_dir_contents)
            request.meta['item'] = item.copy()
            yield request

        next_page = response.xpath("//li[contains(@class, 'hidden-xs')]/a//@href").extract()[1]
        if next_page != '#':
            yield response.follow(next_page, callback=self.parse)

    def parse_dir_contents(self, response):
        # item = LudoItem()
        item = response.meta['item']

        # Getting age, timeOfPlay and numOfPlayers
        item['age'], item['timeOfPlay'], item['numOfPlayers'] = response.xpath("//ul[contains(@class, 'list-inline')]/li/text()").extract()[:3]

        # designer
        item['designer'] = ','.join(response.xpath("//a[./preceding-sibling::h4[1]='Designer']//text()").extract())

        # artist
        item['artist'] = ','.join(response.xpath("//a[./preceding-sibling::h4[1]='Artista']//text()").extract())

        # Domínio
        item['dominio'] = ','.join(response.xpath("//a[./preceding-sibling::h4[1]='Domínio']//text()").extract())

        # Mecânicas
        item['mecanicas'] = ','.join(response.xpath("//a[./preceding-sibling::h4[1]='Mecânica']//text()").extract())

        # Image url
        item['imagem'] = response.xpath("//img[contains(@class, 'img-capa')]//@src").extract()[0]

        # yield item
        yield item
