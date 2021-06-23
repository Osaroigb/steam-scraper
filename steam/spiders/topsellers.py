from scrapy.loader import ItemLoader
from ..items import SteamItem
import scrapy


class TopsellersSpider(scrapy.Spider):

    name = "topsellers"
    allowed_domains = ["store.steampowered.com"]

    def start_requests(self):

        yield scrapy.Request(
            url="https://store.steampowered.com/search/?filter=topsellers",
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
            })

    def parse(self, response):

        # steam_item = SteamItem()
        games = response.xpath("//div[@id='search_resultsRows']/a")

        for game in games:

            loader = ItemLoader(item=SteamItem(), selector=game, response=response)

            loader.add_xpath(field_name="game_url", xpath=".//@href")
            loader.add_xpath(field_name="img_url", xpath=".//div[1]/img/@src")
            loader.add_xpath(field_name="game_name", xpath=".//div[2]/div[1]/span/text()")

            loader.add_xpath(field_name="release_date", xpath="normalize-space(.//div[2]/div[2]/text())")
            loader.add_xpath(field_name="discount_price", xpath="normalize-space(.//div[2]/div[4]/div[2]/text()[2])")
            loader.add_xpath(field_name="discount_rate", xpath="normalize-space(.//div[2]/div[4]/div[1]/span/text())")

            loader.add_value(field_name="original_price", value=game)
            loader.add_xpath(field_name="platform", xpath=".//div[2]/div[1]/p/span/@class")
            loader.add_xpath(field_name="review", xpath="normalize-space(.//div[2]/div[3]/span/@data-tooltip-html)")

            yield loader.load_item()

            # supported_platforms = game.xpath(".//div[2]/div[1]/p/span/@class").getall()
            # ratings = game.xpath("normalize-space(.//div[2]/div[3]/span/@data-tooltip-html)").get()
            # original_price = game.xpath("normalize-space(.//div[2]/div[4]/div[2]//strike/text())").get()
            # discount = game.xpath("normalize-space(.//div[2]/div[4]/div[1]/span/text())").get()

            # steam_item["game_url"] = game.xpath(".//@href").get()
            # steam_item["img_url"] = game.xpath(".//div[1]/img/@src").get()
            # steam_item["game_name"] = game.xpath(".//div[2]/div[1]/span/text()").get()
            # steam_item["release_date"] = game.xpath("normalize-space(.//div[2]/div[2]/text())").get()
            # steam_item["discount_price"] = game.xpath("normalize-space(.//div[2]/div[4]/div[2]/text()[2])").get()

            # steam_item["platform"] = self.get_platforms(list_classes=supported_platforms)
            # steam_item["rating"] = self.remove_html(review_summary=ratings)
            # steam_item["original_price"] = self.get_original_price(price=original_price, selector_obj=game)
            # steam_item["discount_rate"] = self.clean_discount_rate(rate=discount)

            # yield steam_item

        next_page = response.xpath("//a[@class='pagebtn' and text()='>']/@href").get()

        if next_page:

            yield scrapy.Request(
                url=next_page,
                callback=self.parse,
                headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
                }
            )
