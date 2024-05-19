from typing import Union
from fulfillment.models import CargoTypeRange


def get_price_for_cargo_type_express(
    quantity: int, cargo_title: str
) -> Union[float, str]:
    try:
        cargo_type_ranges = CargoTypeRange.objects.filter(
            cargo_type__title=cargo_title, cargo_type__service_type="Express"
        )
        for range in cargo_type_ranges:
            if range.min_quantity <= quantity <= range.max_quantity:
                return range.price
        return "Плотность вашего груза слишком низкая. Свяжитесь с менеджером"
    except CargoTypeRange.DoesNotExist:
        return "Тип груза не найден"


def get_price_for_cargo_type_standart(
    quantity: int, cargo_title: str
) -> Union[float, str]:
    try:
        cargo_type_ranges = CargoTypeRange.objects.filter(
            cargo_type__title=cargo_title, cargo_type__service_type="Standart"
        )
        for range in cargo_type_ranges:
            if range.min_quantity <= quantity <= range.max_quantity:
                return range.price
        return "Плотность вашего груза слишком низкая. Свяжитесь с менеджером"
    except CargoTypeRange.DoesNotExist:
        return "Тип груза не найден"


# Пример использования функций
# quantity = 1500
# cargo_title = "Маркировка"
# print("Цена за Маркировку Express:", get_price_for_cargo_type_express(quantity, cargo_title))
# print("Цена за Маркировку Standart:", get_price_for_cargo_type_standart(quantity, cargo_title))
