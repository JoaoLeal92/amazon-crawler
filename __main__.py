from crawler import Crawler
from html_parser import HtmlDataExtractor
from product import Product

import argparse
import os

parser = argparse.ArgumentParser(description='Amazon products crawler.')
parser.add_argument(
    '-u',
    '--url',
    type=str,
    help='product url'
)
args = parser.parse_args()


def run():
    print("Starting Amazon crawler operation")
    crawler = Crawler(
        driver_path=os.path.abspath(
            '/home/joao/Documents/Projetos/products-monitor/crawlers/driver/chromedriver'),
    )

    crawler.set_driver_options([
        "--disable-extensions",
        "--disable-gpu",
        "--no-sandbox",
        "--headless"
    ])

    print("Startig crawler")
    crawler.start_crawler(implicit_wait_time=10)
    crawler.navigate_to_url("https://www.amazon.com.br/")
    print(f"Navigating to url {args.url}")
    crawler.navigate_to_url(args.url)

    extractor = HtmlDataExtractor(crawler=crawler)

    current_price_identifiers = {
        "xpath": [
            '//span[@id="priceblock_ourprice"]',
            '//span[@id="priceblock_dealprice"]'
        ],
        "class": [
            "priceBlockSavingsString",
            "priceBlockBuyingPriceString"
        ]
    }

    # time.sleep(10)
    print("Searching for price identifier")
    current_price_identifier_type, current_price_identifier_path = extractor.find_price_identifier(
        current_price_identifiers)
    print(current_price_identifier_path)
    print("Extracting current price")
    if current_price_identifier_type == "xpath":
        current_price = extractor.get_product_price_by_xpath(
            current_price_identifier_path)
    elif current_price_identifier_type == "class":
        current_price = extractor.get_current_price_by_class(
            current_price_identifier_path)
    else:
        print("Current price not found")
        current_price = None

    print("Attempting extraction of original price, if exists")
    original_price = extractor.get_original_price_if_exists(
        'priceBlockStrikePriceString')
    print("Attempting extraction of price discount, if exists")
    discount = extractor.get_discount_percentage_if_exists(
        'priceBlockSavingsString')

    product = Product(
        price=current_price,
        original_price=original_price,
        discount=discount
    )

    print(product)

    print("Shutting down crawler")
    crawler.quit()


if __name__ == '__main__':
    run()
    print("Operation completed")
