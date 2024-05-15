from typing import Union

# Цены за кг для ТНП (Express)
tnp_express_prices = {
    (1000, float("inf")): 2.5,
    (800, 999): 2.6,
    (600, 799): 2.7,
    (400, 599): 2.8,
    (350, 399): 2.9,
    (300, 349): 3.0,
    (250, 299): 3.1,
    (200, 249): 3.2,
    (190, 199): 3.3,
    (180, 189): 3.4,
    (170, 179): 3.5,
    (160, 169): 3.6,
    (150, 159): 3.7,
    (140, 149): 3.8,
    (130, 139): 3.9,
    (120, 129): 4.0,
    (110, 119): 4.1,
    (100, 109): 4.2,
    (0, 99): "Плотность вашего груза слишком низкая. Свяжитесь с менеджером",
}

# Цены за кг для ТНП (Standart)
tnp_standart_prices = {
    (1000, float("inf")): 1.6,
    (800, 999): 1.7,
    (600, 799): 1.8,
    (400, 599): 1.9,
    (350, 399): 2.0,
    (300, 349): 2.1,
    (250, 299): 2.2,
    (200, 249): 2.3,
    (190, 199): 2.4,
    (180, 189): 2.5,
    (170, 179): 2.6,
    (160, 169): 2.7,
    (150, 159): 2.8,
    (140, 149): 2.9,
    (130, 139): 3.0,
    (120, 129): 3.1,
    (110, 119): 3.2,
    (100, 109): 3.3,
    (0, 99): "Плотность вашего груза слишком низкая. Свяжитесь с менеджером",
}

# Цены за кг для текстиля (Express)
textile_express_prices = {
    (400, float("inf")): 3.7,
    (350, 399): 3.8,
    (300, 349): 3.9,
    (250, 299): 4.0,
    (200, 249): 4.1,
    (190, 199): 4.2,
    (180, 189): 4.3,
    (170, 179): 4.3,
    (160, 169): 4.4,
    (150, 159): 4.5,
    (140, 149): 4.6,
    (130, 139): 4.7,
    (120, 129): 4.8,
    (110, 119): 4.9,
    (100, 109): 5.0,
    (0, 99): "Плотность вашего груза, слишком низкая. Свяжитесь с менеджером",
}

# Цены за кг для текстиля (Standart)
textile_standart_prices = {
    (380, 400): 3.0,
    (360, 379): 3.1,
    (340, 359): 3.2,
    (320, 339): 3.3,
    (280, 319): 3.4,
    (240, 279): 3.5,
    (200, 239): 3.6,
    (0, 199): "Плотность вашего груза слишком низкая. Свяжитесь с менеджером",
}

# Цены на упаковку для Маркировки
marking_prices = {
    (5000, float("inf")): 4,
    (2000, 4999): 5,
    (1000, 1999): 6,
    (500, 999): 7,
    (100, 499): 7,
    (0, 99): 0,
}

# Цены на упаковку для Маркировки двойной
double_marking_prices = {
    (5000, float("inf")): 7,
    (2000, 4999): 8,
    (1000, 1999): 10,
    (500, 999): 12,
    (100, 499): 12,
    (0, 99): 0,
}

# Цены на упаковку для Упаковки Стандартной
standard_packing_prices = {
    (5000, float("inf")): 4,
    (2000, 4999): 5,
    (1000, 1999): 6,
    (500, 999): 7,
    (100, 499): 7,
    (0, 99): 0,
}

# Цены на упаковку для Сборки
assembly_prices = {
    (5000, float("inf")): 10,
    (2000, 4999): 11,
    (1000, 1999): 13,
    (500, 999): 15,
    (100, 499): 15,
    (0, 99): 0,
}

# Цены на упаковку для Биркования
tagging_prices = {
    (5000, float("inf")): 4,
    (2000, 4999): 5,
    (1000, 1999): 6,
    (500, 999): 6,
    (100, 499): 6,
    (0, 99): 0,
}

# Цены на упаковку для Вложений
inserts_prices = {
    (5000, float("inf")): 3,
    (2000, 4999): 3.5,
    (1000, 1999): 4,
    (500, 999): 5,
    (100, 499): 5,
    (0, 99): 0,
}

# Цены на упаковку для Укладки
stacking_prices = {
    (5000, float("inf")): 1,
    (2000, 4999): 2,
    (1000, 1999): 2.5,
    (500, 999): 3,
    (100, 499): 4,
    (0, 99): 0,
}


def calculate_price_per_kg_for_tnp_express(density) -> Union[float, str]:
    for (min_density, max_density), price in tnp_express_prices.items():
        if min_density <= density <= max_density:
            return price

    return None


def calculate_price_per_kg_for_tnp_standart(density) -> Union[float, str]:
    for (min_density, max_density), price in tnp_standart_prices.items():
        if min_density <= density <= max_density:
            return price

    return None


def calculate_price_per_kg_for_textile_express(density) -> Union[float, str]:
    for (min_density, max_density), price in textile_express_prices.items():
        if min_density <= density <= max_density:
            return price
    return None


def calculate_price_per_kg_for_textile_standart(density) -> Union[float, str]:
    for (min_density, max_density), price in textile_standart_prices.items():
        if min_density <= density <= max_density:
            return price
    return None


def calculate_packing_price(quantity, packing_type_prices) -> Union[float, str]:
    for (min_qty, max_qty), price in packing_type_prices.items():
        if min_qty <= quantity <= max_qty:
            return price
    return None


quantity = 1500
print("Цена за Маркировку:", calculate_packing_price(quantity, marking_prices))
print(
    "Цена за Маркировку двойную:",
    calculate_packing_price(quantity, double_marking_prices),
)
print(
    "Цена за Упаковку Стандартную:",
    calculate_packing_price(quantity, standard_packing_prices),
)
print("Цена за Сборку:", calculate_packing_price(quantity, assembly_prices))
print("Цена за Биркование:", calculate_packing_price(quantity, tagging_prices))
print("Цена за Вложения:", calculate_packing_price(quantity, inserts_prices))
print("Цена за Укладку:", calculate_packing_price(quantity, stacking_prices))
