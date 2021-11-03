from crawler import Crawler
from html_parser import HtmlDataExtractor
from product import Product
from logs import Logs

import argparse
import os

from dotenv import dotenv_values

parser = argparse.ArgumentParser(description='Amazon products crawler.')
parser.add_argument(
    '-u',
    '--url',
    type=str,
    help='product url'
)
args = parser.parse_args()


def run():
    config = dotenv_values()
    logs = Logs(config)

    logs.write_info(config['CRAWLER_NAME'],
                    "Starting Amazon crawler operation")
    crawler = Crawler(
        driver_path=os.path.abspath(
            config["CHROMEDRIVER_PATH"]),
    )

    crawler.set_driver_options([
        "--disable-extensions",
        "--disable-gpu",
        "--no-sandbox",
        "--headless"
    ])

    logs.write_info(config['CRAWLER_NAME'],
                    "Starting crawler")
    crawler.start_crawler(implicit_wait_time=10)

    logs.write_info(config['CRAWLER_NAME'],
                    f"Navigating to url {args.url}")
    crawler.navigate_to_url("https://www.amazon.com.br/")
    crawler.navigate_to_url(args.url)

    extractor = HtmlDataExtractor(crawler=crawler, logs=logs, config=config)

    current_price_identifiers = {
        "xpath": [
            '//span[@id="priceblock_ourprice"]',
            '//span[@id="priceblock_dealprice"]',
            '//span[@id="priceblock_saleprice"]',
            '//span[contains(@class, "a-price")]',
            '//span[contains(@class, "a-size-medium")]',
            '//span[contains(@class, "apexPriceToPay")]',
            '//span[contains(@class, "a-text-price")]'
        ],
        "class": [
            "priceBlockSavingsString"
        ]
    }

    logs.write_info(config['CRAWLER_NAME'],
                    "Searching for price identifier")
    current_price_identifier_type, current_price_identifier_path = extractor.find_price_identifier(
        current_price_identifiers)

    logs.write_info(config['CRAWLER_NAME'],
                    "Extracting current price")
    if current_price_identifier_type == "xpath":
        current_price = extractor.get_product_price_by_xpath(
            current_price_identifier_path)
    elif current_price_identifier_type == "class":
        current_price = extractor.get_current_price_by_class(
            current_price_identifier_path)
    else:
        logs.write_error(config['CRAWLER_NAME'],
                         "Current price not found")
        current_price = None

    logs.write_info(config['CRAWLER_NAME'],
                    "Attempting extraction of original price, if exists")
    original_price = extractor.get_original_price_if_exists(
        'priceBlockStrikePriceString')

    logs.write_info(config['CRAWLER_NAME'],
                    "Attempting extraction of price discount, if exists")
    discount = extractor.get_discount_percentage_if_exists(
        'priceBlockSavingsString')

    if original_price is None:
        original_price = current_price

    product = Product(
        price=current_price,
        original_price=original_price,
        discount=discount,
        link=args.url.strip()
    )

    print(product)

    logs.write_info(config['CRAWLER_NAME'],
                    "Shutting down crawler")
    crawler.quit()
    logs.write_info(config['CRAWLER_NAME'],
                    "Operation completed")


if __name__ == '__main__':
    run()
