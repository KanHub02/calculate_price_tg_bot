def format_ff_response(data):
    """
    Преобразует ответ сервера в читаемый формат.

    :param data: словарь с данными от сервера.
    :return: строка с отформатированным текстом.
    """
    if isinstance(data, dict):
        formatted_response = (
            f"Товар: {data['product_title']}\n"
            f"Кол-во: {data['quantity']}\n"
            f"Вид Маркировки: {data['marking_type_title']}\n"
            f"Честный знак: {'Да' if data['honest_sign'] else 'Нет'}\n"
            f"Упаковка: {data['package_title']}\n"
            f"Вид Упаковки: {data['packaging_size']}\n"
            f"Биркование: {'Да' if data['need_taging'] else 'Нет'}\n"
            f"Вложения: {'Да' if data['need_attachment'] else 'Нет'}\n"
            f"Кол-во коробов: {data['count_of_boxes']}\n\n"
            f"Цена работы фф на 1 единицу: {data['per_price']}\n"
            f"Цена материалов на 1 ед: {data['per_price_material']}\n"
            f"Цена транзита на 1 единицу: {data['per_price_transit']}\n"
        )
        return formatted_response
    else:
        return "Что то пошло не так"


def format_logistic_request(data):
    """
    Преобразует данные логистического запроса в читаемый формат.
    :param data: словарь с данными логистического запроса от сервера.
    :return: строка с отформатированным текстом.
    """
    express_price = round(
        float(data["total_express"]), 2
    )  # Приводим к числу и округляем
    standard_price = round(float(data["total_standard"]), 2)
    packaging_cost = round(float(data["packaging_cost"]), 2)
    insurance_cost = round(float(data["insurance_cost"]), 2)
    weight = round(float(data["weight"]), 2)
    cube = round(float(data["cube"]), 2)

    formatted_response = (
        f"Вид товара: {data['cargo_type']}\n"
        f"Вес: {weight} кг\n"
        f"Куб: {cube} куб. м.\n"
        f"Тип упаковки груза: {data['packaging_type']}\n"
        f"Стоимость упаковки: {packaging_cost} ¥\n"
        f"Стоимость страховки: {insurance_cost} $\n\n"
        "Цены на услуги:\n"
    )

    if data["services_pricing"]:
        for service in data["services_pricing"]:
            price = (
                f"{round(float(service['price']), 2)} $"
                if isinstance(service["price"], float)
                else service["price"]
            )
            formatted_response += f"- {service['service_name']}: {price}\n"
    else:
        formatted_response += "Цены на услуги: не указаны\n"

    formatted_response += (
        f"\nИтого Express: {express_price} $\n" f"Итого Standard: {standard_price} $"
    )

    return formatted_response


def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


async def is_not_empty(data, state):
    await state.finish()
    return bool(data)
