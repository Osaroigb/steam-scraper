# Define here the models for your scraped items

# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy.loader.processors import TakeFirst, MapCompose
from w3lib.html import remove_tags
import scrapy


def get_original_price(selector_obj):

    price = selector_obj.xpath("normalize-space(.//div[2]/div[4]/div[2]//strike/text())").get()

    if price == "":
        return selector_obj.xpath("normalize-space(.//div[2]/div[4]/div[2]/text()[1])").get()
    else:
        return price


def get_release_date(date):

    if date == "":
        return "No date"
    else:
        return date


def get_discount_price(price):

    if price == "":
        return "$0.00"
    else:
        return price


def clean_discount_rate(rate):

    if rate == "":
        return "0%"
    else:
        return rate[1:]


def get_platforms(platform_class):

    platforms = []

    # for platform_class in platform_classes:

    platform = platform_class.split()[-1]

    if platform == "win":
        platforms.append("Windows")
    elif platform == "mac":
        platforms.append("Mac OS")
    elif platform == "linux":
        platforms.append("Linux")
    elif platform == "vr_supported":
        platforms.append("VR")

    return platforms


def remove_html(review_summary):

    cleaned_summary = remove_tags(text=review_summary)

    if cleaned_summary == "":
        return "No review"
    else:
        return cleaned_summary


class SteamItem(scrapy.Item):

    game_url = scrapy.Field(
        output_processor=TakeFirst()
    )

    img_url = scrapy.Field(
        output_processor=TakeFirst()
    )

    game_name = scrapy.Field(
        output_processor=TakeFirst()
    )

    release_date = scrapy.Field(
        input_processor=MapCompose(get_release_date),
        output_processor=TakeFirst()
    )

    discount_price = scrapy.Field(
        input_processor=MapCompose(get_discount_price),
        output_processor=TakeFirst()
    )

    discount_rate = scrapy.Field(
        input_processor=MapCompose(clean_discount_rate),
        output_processor=TakeFirst()
    )

    original_price = scrapy.Field(
        input_processor=MapCompose(get_original_price),
        output_processor=TakeFirst()
    )

    platform = scrapy.Field(
        input_processor=MapCompose(get_platforms)
    )

    review = scrapy.Field(
        input_processor=MapCompose(remove_html),
        output_processor=TakeFirst()
    )
