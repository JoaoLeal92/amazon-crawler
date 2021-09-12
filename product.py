from dataclasses import dataclass


@dataclass
class Product:
    price: int
    original_price: int
    discount: str
    link: str
