from config import logger
from aiogram.utils.markdown import text, bold, escape_md

def format_ff_response(data):
    """
    Преобразует ответ сервера в читаемый формат.
    
    :param data: словарь с данными от сервера.
    :return: строка с отформатированным текстом.
    """
    logger.info(data)
    if isinstance(data, dict):
        formatted_response = text(
            bold("🛒 Товар:") + f" {escape_md(data['product_title'])}",
            bold("📦 Кол-во:") + f" {escape_md(str(data['quantity']))}",
            bold("🔍 Проверка на брак:") + f" {'Да' if data.get('check_defects_title') else 'Нет'}",
            bold("🏷 Вид Маркировки:") + f" {'Да' if data.get('marking_type_title') else 'Нет'}",
            bold("✅ Честный знак:") + f" {'Да' if data.get('honest_sign') else 'Нет'}",
            bold("📦 Упаковка:") + f" {'Да' if data.get('package_title') else 'Нет'}",
            bold("📏 Вид Упаковки:") + f" {'Да' if data.get('packaging_size') else 'Нет'}",
            bold("🏷 Биркование:") + f" {'Да' if data.get('need_taging') else 'Нет'}",
            bold("📎 Вложения:") + f" {'Да' if data.get('need_attachment') else 'Нет'}",
            bold("📦 Кол-во коробов:") + f" {escape_md(str(data['count_of_boxes']))}",
            "",
            bold("💰 Цена работы фф на 1 единицу:") + f" {escape_md(str(data['per_price_ff']))}",
            bold("💰 Цена материалов на 1 ед:") + f" {escape_md(str(data['per_price_material']))}",
            bold("💰 Цена транзита на 1 единицу:") + f" {escape_md(str(data['per_price_transit']))}",
            sep="\n"
        )
        return formatted_response
    else:
        return "Что-то пошло не так"

def format_logistic_request(data):
    """
    Преобразует данные логистического запроса в читаемый формат.
    :param data: словарь с данными логистического запроса от сервера.
    :return: строка с отформатированным текстом.
    """
    express_price = round(float(data["total_express"]), 2)
    standard_price = round(float(data["total_standard"]), 2)
    packaging_cost = round(float(data["packaging_cost"]), 2)
    insurance_cost = round(float(data["insurance_cost"]), 2)
    weight = round(float(data["weight"]), 2)
    cube = round(float(data["cube"]), 2)

    formatted_response = text(
        bold("Вид товара:") + f" {data['cargo_type']}",
        bold("Вес:") + f" {weight} кг",
        bold("Куб:") + f" {cube} куб. м.",
        bold("Тип упаковки груза:") + f" {data['packaging_type']}",
        bold("Стоимость упаковки:") + f" {packaging_cost} ¥",
        bold("Стоимость страховки:") + f" {insurance_cost} $",
        "",
        bold("Цены на услуги:"),
        sep="\n"
    )

    if data["services_pricing"]:
        for service in data["services_pricing"]:
            price = (
                f"{round(float(service['price']), 2)} $"
                if is_float(service["price"])
                else service["price"]
            )
            formatted_response += f"\n- {service['service_name']}: {price}"
    else:
        formatted_response += "\nЦены на услуги: не указаны"

    formatted_response += (
        f"\n\n{bold('Итого Express:')} {express_price} $\n{bold('Итого Standard:')} {standard_price} $"
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
