import re
from typing import List, Dict

from crawler import Crawler
from logs import Logs

from selenium.common.exceptions import NoSuchElementException


class HtmlDataExtractor:
    def __init__(self, crawler, logs, config):
        self.crawler: Crawler = crawler
        self.logs: Logs = logs
        self.config: Dict[str, str] = config

    def find_price_identifier(self, identifier_map: Dict[str, List[str]]) -> str:
        for key, identifiers in identifier_map.items():
            if key == "xpath":
                for identifier in identifiers:
                    try:
                        element = self.crawler.driver.find_element_by_xpath(
                            identifier)
                        if element:
                            return key, identifier
                    except NoSuchElementException:
                        pass
            elif key == "class":
                for identifier in identifiers:
                    try:
                        element = self.crawler.driver.find_element_by_class_name(
                            identifier)
                        if element:
                            return key, identifier
                    except NoSuchElementException:
                        pass

        return None, None

    def get_product_price_by_xpath(self, price_path: str) -> int:
        try:
            product_price = self._get_element_text_by_xpath(price_path)
            formatted_price = self._price_string_to_float(product_price)

            return formatted_price
        except NoSuchElementException:
            return None
        except ValueError:
            self.logs.write_error(
                self.config['CRAWLER_NAME'], "Erro na conversão de preço para inteiro")
            return None
        except Exception as e:
            self.logs.write_error(
                self.config['CRAWLER_NAME'], f"Ocorreu o seguinte erro: {e}")
            return None

    def _get_element_text_by_xpath(self, xpath: str) -> str:
        html_element = self.crawler.driver.find_element_by_xpath(xpath)
        html_text = html_element.text

        return html_text

    def _price_string_to_float(self, price_string: str) -> int:
        formatted_string = price_string.replace(
            "R$", "").replace(".", "").replace(",", "")

        int_price = int(formatted_string.strip())
        return int_price

    def get_original_price_if_exists(self, original_price_class: str) -> int:
        try:
            original_price_value = self._get_element_text_by_class_name(
                original_price_class)
            formatted_price = self._price_string_to_float(original_price_value)

            return formatted_price
        except NoSuchElementException:
            return None
        except ValueError:
            self.logs.write_error(
                self.config['CRAWLER_NAME'], "Erro na conversão de preço para inteiro")
            return None
        except Exception as e:
            self.logs.write_error(
                self.config['CRAWLER_NAME'], f"Ocorreu o seguinte erro: {e}")
            return None

    def get_discount_percentage_if_exists(self, discount_class: str) -> str:
        try:
            discount_value = self._get_element_text_by_class_name(
                discount_class)

            if discount_value:
                discount_percentage = self._extract_percentage_string(
                    discount_value)
                return discount_percentage

            return discount_value
        except NoSuchElementException:
            return None
        except IndexError as e:
            return None
        except Exception as e:
            self.logs.write_error(
                self.config['CRAWLER_NAME'], f"Ocorreu o seguinte erro: {e}")
            return None

    def _get_element_text_by_class_name(self, class_name: str) -> str:
        html_element = self.crawler.driver.find_element_by_class_name(
            class_name)
        html_text = html_element.text

        return html_text

    def _extract_percentage_string(self, original_string: str) -> str:
        match_string = '\d{1,2}%'

        matches = re.findall(match_string, original_string)
        match = matches[0]

        return match

    def get_current_price_by_class(self, class_name: str) -> int:
        try:
            current_price_value = self._get_element_text_by_class_name(
                class_name)
            formatted_price = self._price_string_to_float(current_price_value)

            return formatted_price
        except NoSuchElementException:
            return None
        except ValueError:
            self.logs.write_error(
                self.config['CRAWLER_NAME'], "Erro na conversão de preço para inteiro")
            return None
        except Exception as e:
            self.logs.write_error(
                self.config['CRAWLER_NAME'], f"Ocorreu o seguinte erro: {e}")
            return None
