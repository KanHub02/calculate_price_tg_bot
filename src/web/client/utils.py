from typing import Union
from logistic.models import CargoType, CargoTypeRange, CargoServiceType


# Utility function to calculate the price
def calculate_price(service_name, cargo_type_title, density):
    try:
        service_type = CargoServiceType.objects.get(name=service_name, cargo_type__title=cargo_type_title)
        price_range = CargoTypeRange.objects.filter(
            cargo_service=service_type,
            min_density__lte=density,
            max_density__gte=density,
        ).first()

        if price_range:
            return price_range.price
        else:
            return "Плотность вашего груза слишком низкая или высокая. Свяжитесь с менеджером."
    except CargoServiceType.DoesNotExist:
        return "Сервис или тип груза не найден."
