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
            bold("🔍 Проверка на брак:")
            + f" {'Да' if data.get('check_defects_title') else 'Нет'}",
            bold("🏷 Вид Маркировки:")
            + f" {'Да' if data.get('marking_type_title') else 'Нет'}",
            bold("✅ Честный знак:") + f" {'Да' if data.get('honest_sign') else 'Нет'}",
            bold("📦 Упаковка:") + f" {'Да' if data.get('package_title') else 'Нет'}",
            bold("📏 Вид Упаковки:")
            + f" {'Да' if data.get('packaging_size') else 'Нет'}",
            bold("🏷 Биркование:") + f" {'Да' if data.get('need_taging') else 'Нет'}",
            bold("📎 Вложения:") + f" {'Да' if data.get('need_attachment') else 'Нет'}",
            bold("📦 Кол-во коробов:") + f" {escape_md(str(data['count_of_boxes']))}",
            "",
            bold("💰 Цена работы фф на 1 единицу:")
            + f" {escape_md(str(data['per_price_ff']))}",
            bold("💰 Цена материалов на 1 ед:")
            + f" {escape_md(str(data['per_price_material']))}",
            bold("💰 Цена транзита на 1 единицу:")
            + f" {escape_md(str(data['per_price_transit']))}",
            sep="\n",
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
    logger.info(data)

    express_price = round(float(data.get("Итого Express", 0)), 2)
    standard_price = round(float(data.get("Итого Standart", 0)), 2)
    packaging_cost = round(float(data.get("Упаковка", 0)), 2)
    insurance_cost = round(float(data.get("Страховка", 0)), 2)
    weight = round(float(data.get("Вес", 0)), 2)
    volume = round(float(data.get("Куб", 0)), 2)

    formatted_response = text(
        bold("📦 Вид товара:") + f" {escape_md(data.get('Вид товара', 'Не указано'))}",
        bold("⚖️ Вес:") + f" {weight} кг",
        bold("📏 Куб:") + f" {volume} куб. м",
        bold("📦 Упаковка:") + f" {packaging_cost} ¥",
        bold("💰 Страховка:") + f" {insurance_cost} $",
        "",
        bold("🚀 Express:") + f" {express_price} $",
        bold("🚚 Standart:") + f" {standard_price} $",
        "",
        bold("Итого Express:")
        + f" {express_price + packaging_cost + insurance_cost} $",
        bold("Итого Standart:")
        + f" {standard_price + packaging_cost + insurance_cost} $",
        sep="\n",
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
