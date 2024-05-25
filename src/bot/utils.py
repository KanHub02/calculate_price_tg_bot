def format_ff_response(data):
    """
    Преобразует ответ сервера в читаемый формат.

    :param data: словарь с данными от сервера.
    :return: строка с отформатированным текстом.
    """
    if isinstance(data,dict):
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
    formatted_response = (
        f"Тип груза: {data['cargo_type']}\n"
        f"Тип упаковки груза: {data['cargo_package_type']}\n"
        f"Количество: {data['quantity']}\n"
        f"Вес: {data['weight']} кг\n"
        f"Стоимость страховки: {data['insurance_cost']} руб.\n"
    )

    # Если список услуг по ценообразованию не пуст, добавляем его в ответ
    if data['services_pricing']:
        formatted_response += "Цены на услуги:\n"
        for service in data['services_pricing']:
            formatted_response += f"- {service['service_name']}: {service['price']} руб.\n"
    else:
        formatted_response += "Цены на услуги: не указаны\n"

    return formatted_response