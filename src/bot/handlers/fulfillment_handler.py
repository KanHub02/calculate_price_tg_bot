from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils.exceptions import MessageToDeleteNotFound
from aiogram.types import ParseMode

from api.fulfillment_api import (
    fetch_marking_types,
    fetch_packaging_options,
    fetch_packaging_sizes,
    fetch_warehouses,
    create_fulfillment_request,
    get_ff_detail,
    get_check_defect_type,
)
from keyboards.fulfillment_kb import (
    select_marking_type,
    select_packaging_option,
    select_packaging_sizes,
    select_warehouse_keyboard,
    select_checkdefect_type,
)
from keyboards.base_kb import yes_no_keyboard, main_menu_keyboard, answerkb
from utils import is_float, format_ff_response

from config import bot, logger


async def generate_defect_dict(defect_data):
    defect_data_dict = {}
    for i in defect_data:
        defect_data_dict[i['title']] = i['id']
    return defect_data_dict


async def fetch_and_check(api_call, error_message):
    result = await api_call()
    if len(result) <= 0:
        return None, error_message
    return result, ""


class FulfillmentForm(StatesGroup):
    product_name = State()
    quantity = State()
    need_defect_check = State()
    set_defect_check = State()
    ask_marking_type = State()
    marking_type = State()
    honest_sign = State()
    ask_packaging = State()
    packaging = State()
    packaging_size = State()
    tagging = State()
    inserts = State()
    box_quantity = State()
    warehouse = State()


async def delete_last_message(user_id, chat_id, state: FSMContext):
    user_data = await state.get_data()
    if "last_message_id" in user_data:
        try:
            await bot.delete_message(chat_id, user_data["last_message_id"])
        except MessageToDeleteNotFound as e:
            logger.debug(e)


async def calculate_fulfillment_start(
    callback_query: types.CallbackQuery, state: FSMContext
):
    await bot.answer_callback_query(callback_query.id)
    await delete_last_message(
        callback_query.from_user.id, callback_query.message.chat.id, state
    )
    message = await bot.send_message(
        callback_query.from_user.id, "Введите наименование товара:"
    )
    await state.update_data(last_message_id=message.message_id)
    await FulfillmentForm.next()


async def set_product_name(message: types.Message, state: FSMContext):
    await delete_last_message(message.from_user.id, message.chat.id, state)
    await state.update_data(product_name=message.text)
    new_message = await message.reply("Введите количество товара:")
    await state.update_data(last_message_id=new_message.message_id)
    await FulfillmentForm.next()


async def set_quantity(message: types.Message, state: FSMContext):
    await delete_last_message(
        message.from_user.id, message.chat.id, state
    )

    if not is_float(message.text):
        new_message = await message.reply("Пожалуйста, введите правильное числовое количество.")
        await state.update_data(last_message_id=new_message.message_id)
        return
    await state.update_data(quantity=float(message.text))

    new_message = await message.reply(
        "Нужна ли проверка на брак?", reply_markup=answerkb()
    )
    await state.update_data(last_message_id=new_message.message_id)
    await FulfillmentForm.next()


async def ask_need_defect_check(message: types.Message, state: FSMContext):
    await delete_last_message(
        message.from_user.id, message.chat.id, state
    )
    if message.text.lower() == "да":
        chech_defets_types, error = await fetch_and_check(
            get_check_defect_type,
            "Типы проверки не найдены, пожалуйста, попробуйте позже.",
        )
        if error:
            await bot.send_message(
                message.from_user.id, error, reply_markup=main_menu_keyboard()
            )
            await state.finish()
            return
        new_message = await bot.send_message(
            message.from_user.id, "Выберите тип проверки:", reply_markup=select_checkdefect_type(chech_defets_types)
        )
        await state.update_data(last_message_id=new_message.message_id)
        await FulfillmentForm.next()
    elif message.text.lower() == "нет":
        new_message = await bot.send_message(
            message.from_user.id, "Нужна ли маркировка?", reply_markup=answerkb()
        )
        await state.update_data(last_message_id=new_message.message_id)
        await FulfillmentForm.ask_marking_type.set()
    else:
        new_message = await message.reply(
            "Нужна ли проверка на брак? Введите Да или Нет", reply_markup=answerkb()
        )
        await state.update_data(last_message_id=new_message.message_id)
        return


async def set_need_defect_check(message: types.Message, state:FSMContext):
    await delete_last_message(
        message.from_user.id, message.chat.id, state
    )
    chech_defets_types, error = await fetch_and_check(
        get_check_defect_type,
        "Типы проверки не найдены, пожалуйста, попробуйте позже.",
    )
    if error:
        await bot.send_message(
            message.from_user.id, error, reply_markup=main_menu_keyboard()
        )
        await state.finish()
        return

    defect_dict = await generate_defect_dict(chech_defets_types)
    if message.text in defect_dict:
        await state.update_data(defect_check_id=defect_dict[message.text])
        new_message = await bot.send_message(
            message.from_user.id, "Нужна ли маркировка?", reply_markup=answerkb()
        )
        await state.update_data(last_message_id=new_message.message_id)
        await FulfillmentForm.next()
    else:
        new_message = await bot.send_message(
            message.from_user.id, "Выберите из предложенного списка:",
            reply_markup=select_checkdefect_type(chech_defets_types)
        )
        await state.update_data(last_message_id=new_message.message_id)
        return


async def ask_marking_type(message: types.Message, state: FSMContext):
    await delete_last_message(
        message.from_user.id, message.chat.id, state
    )
    if message.text.lower() == "да":
        marking_types, error = await fetch_and_check(
            fetch_marking_types, "Типы маркировки не найдены, пожалуйста, попробуйте позже."
        )
        if error:
            await bot.send_message(
                message.from_user.id, error, reply_markup=main_menu_keyboard()
            )
            await state.finish()
            return
        new_message = await bot.send_message(
            message.from_user.id, "Выберите тип маркировки1:", reply_markup=select_marking_type(marking_types)
        )
        await state.update_data(last_message_id=new_message.message_id)
        await FulfillmentForm.next()
    elif message.text.lower() == "нет":
        new_message = await bot.send_message(
            message.from_user.id, "Требуется ли Честный знак?:", reply_markup=answerkb()
        )
        await state.update_data(last_message_id=new_message.message_id)
        await FulfillmentForm.honest_sign.set()
    else:
        new_message = await message.reply(
            "Нужна ли маркировка? Введите Да или Нет", reply_markup=answerkb()
        )
        await state.update_data(last_message_id=new_message.message_id)
        return


async def set_marking_type(message: types.Message, state: FSMContext):
    await delete_last_message(
        message.from_user.id, message.chat.id, state
    )
    marking_types, error = await fetch_and_check(
        fetch_marking_types, "Типы маркировки не найдены, пожалуйста, попробуйте позже."
    )
    if error:
        await bot.send_message(
            message.from_user.id, error, reply_markup=main_menu_keyboard()
        )
        await state.finish()
        return

    marking_dict = await generate_defect_dict(marking_types)
    logger.info(marking_types)
    if message.text in marking_dict:
        await state.update_data(defect_check_id=marking_dict[message.text])
        new_message = await bot.send_message(
            message.from_user.id, "Требуется ли Честный знак?", reply_markup=answerkb()
        )
        await state.update_data(last_message_id=new_message.message_id)
        await FulfillmentForm.next()
    else:
        new_message = await bot.send_message(
            message.from_user.id, "Выберите из предложенного списка:",
            reply_markup=select_marking_type(marking_types)
        )
        await state.update_data(last_message_id=new_message.message_id)
        return


async def set_honest_sign(message: types.Message, state: FSMContext):
    await delete_last_message(
        message.from_user.id, message.chat.id, state
    )
    if message.text.lower() == "да":
        await state.update_data(honest_sign=True)
        new_message = await message.reply(
            "Нужно ли упаковать товар?", reply_markup=answerkb()
        )
        await state.update_data(last_message_id=new_message.message_id)
        await FulfillmentForm.next()
    elif message.text.lower() == 'нет':
        await state.update_data(honest_sing=False)
        new_message = await message.reply(
            "Нужно ли упаковать товар?", reply_markup=answerkb()
        )
        await state.update_data(last_message_id=new_message.message_id)
        await FulfillmentForm.next()
    else:
        new_message = await message.reply(
            "Требуется ли Честный знак? Да или Нет", reply_markup=answerkb()
        )
        await state.update_data(last_message_id=new_message.message_id)
        return


async def ask_packaging(message: types.Message, state: FSMContext):
    await delete_last_message(
        message.from_user.id, message.chat.id, state
    )
    if message.text.lower() == "да":
        packaging_options = await fetch_packaging_options()
        if not packaging_options:
            await message.reply(
                "Варианты упаковки не найдены, пожалуйста, попробуйте позже."
            )
            await state.finish()
            return
        keyboard = select_packaging_option(packaging_options)
        new_message = await bot.send_message(
            message.from_user.id, "Выберите вид упаковки:", reply_markup=keyboard
        )
        await state.update_data(last_message_id=new_message.message_id)
        await FulfillmentForm.next()
    elif message.text.lower() == "нет":
        new_message = await bot.send_message(
            message.from_user.id, "Требуется ли Честный знак?:", reply_markup=answerkb()
        )
        await state.update_data(last_message_id=new_message.message_id)
        await FulfillmentForm.honest_sign.set()
    else:
        new_message = await message.reply(
            "Нужна ли маркировка? Введите Да или Нет", reply_markup=answerkb()
        )
        await state.update_data(last_message_id=new_message.message_id)
        return


async def set_packaging(callback_query: types.CallbackQuery, state: FSMContext):
    packaging_id = callback_query.data.split("_")[1]
    sizes = await fetch_packaging_sizes(packaging_id)
    if not sizes:
        await callback_query.message.reply(
            "Размеры для этой упаковки не доступны, пожалуйста, попробуйте позже."
        )
        await state.finish()
        return
    keyboard = select_packaging_sizes(sizes)
    await delete_last_message(
        callback_query.from_user.id, callback_query.message.chat.id, state
    )
    message = await bot.send_message(
        callback_query.from_user.id, "Выберите размер упаковки:", reply_markup=keyboard
    )
    await state.update_data(
        packaging_id=packaging_id, last_message_id=message.message_id
    )
    await FulfillmentForm.packaging_size.set()


async def ask_box_quantity(user_id, state: FSMContext):
    new_message = await bot.send_message(
        user_id, "Сколько помещается штук в короб 60x40x40?"
    )
    await state.update_data(last_message_id=new_message.message_id)
    await FulfillmentForm.next()


async def set_box_quantity(message: types.Message, state: FSMContext):
    if not is_float(message.text):
        await message.reply("Пожалуйста, введите действительное количество.")
        return
    await state.update_data(box_quantity=int(float(message.text)))
    packaging_options = await fetch_packaging_options()
    if not packaging_options:
        await message.reply(
            "Варианты упаковки не найдены, пожалуйста, попробуйте позже."
        )
        await state.finish()
        return
    keyboard = select_packaging_option(packaging_options)
    await delete_last_message(message.from_user.id, message.chat.id, state)
    new_message = await message.reply("Выберите вид упаковки:", reply_markup=keyboard)
    await state.update_data(last_message_id=new_message.message_id)
    await FulfillmentForm.packaging.set()

async def set_packaging_size(callback_query: types.CallbackQuery, state: FSMContext):
    size = callback_query.data.split("_")[1]
    await state.update_data(packaging_size=size)
    await delete_last_message(
        callback_query.from_user.id, callback_query.message.chat.id, state
    )
    keyboard = yes_no_keyboard()
    message = await bot.send_message(
        callback_query.from_user.id, "Нужно ли биркование?", reply_markup=keyboard
    )
    await state.update_data(last_message_id=message.message_id)
    await FulfillmentForm.tagging.set()


async def set_tagging(callback_query: types.CallbackQuery, state: FSMContext):
    tagging = callback_query.data == "yes"
    await state.update_data(tagging=tagging)
    await delete_last_message(
        callback_query.from_user.id, callback_query.message.chat.id, state
    )
    keyboard = yes_no_keyboard()
    message = await bot.send_message(
        callback_query.from_user.id, "Нужны ли вложения?", reply_markup=keyboard
    )
    await state.update_data(last_message_id=message.message_id)
    await FulfillmentForm.inserts.set()


async def set_inserts(callback_query: types.CallbackQuery, state: FSMContext):
    inserts = callback_query.data == "yes"
    await state.update_data(inserts=inserts)
    warehouses, error = await fetch_and_check(
        fetch_warehouses,
        "Информация о складе не найдена, пожалуйста, попробуйте позже.",
    )
    if error:
        await callback_query.message.reply(error)
        await state.finish()
        return

    keyboard = select_warehouse_keyboard(warehouses)

    await delete_last_message(
        callback_query.from_user.id, callback_query.message.chat.id, state
    )
    message = await bot.send_message(
        callback_query.from_user.id, "Выберите склад:", reply_markup=keyboard
    )
    await state.update_data(last_message_id=message.message_id)
    await FulfillmentForm.warehouse.set()



async def set_warehouse(callback_query: types.CallbackQuery, state: FSMContext):
    warehouse_id = callback_query.data.split("_")[1]
    await state.update_data(warehouse_id=warehouse_id)
    await delete_last_message(
        callback_query.from_user.id, callback_query.message.chat.id, state
    )
    user_data = await state.get_data()
    defect_check_id = user_data.get("defect_check_id", None)
    api_data = {
        "tg_client_id": callback_query.from_user.id,
        "defect_check_id": defect_check_id,
        "marking_type_id": user_data["marking_type_id"],
        "package_id": user_data["packaging_id"],
        "packaging_size": user_data["packaging_size"],
        "stock_id": user_data["warehouse_id"],
        "product_title": user_data["product_name"],
        "quantity": user_data["quantity"],
        "need_attachment": user_data["inserts"],
        "need_taging": user_data["tagging"],
        "count_of_boxes": user_data["box_quantity"],
        "honest_sign": user_data["honest_sign"],
    }
    ff_id = await create_fulfillment_request(api_data)
    ff_data = await get_ff_detail(ff_id.get("ff_id"))
    keyboard = main_menu_keyboard()
    response_data = format_ff_response(ff_data)
    await callback_query.message.answer(response_data, parse_mode=ParseMode.MARKDOWN_V2)
    await callback_query.message.answer("Выберите действие:", reply_markup=keyboard)
    await state.finish()


def register_fulfillment_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(
        calculate_fulfillment_start, lambda c: c.data == "calculate_fulfillment"
    )
    dp.register_message_handler(set_product_name, state=FulfillmentForm.product_name)
    dp.register_message_handler(set_quantity, state=FulfillmentForm.quantity)
    dp.register_message_handler(ask_need_defect_check, state=FulfillmentForm.need_defect_check)
    dp.register_message_handler(set_need_defect_check, state=FulfillmentForm.set_defect_check)
    dp.register_message_handler(
        ask_marking_type, state=FulfillmentForm.ask_marking_type
    )
    dp.register_message_handler(
        set_marking_type, state=FulfillmentForm.marking_type
    )
    dp.register_callback_query_handler(
        set_honest_sign, state=FulfillmentForm.honest_sign
    )
    dp.register_message_handler(ask_packaging, state=FulfillmentForm.ask_packaging)
    dp.register_callback_query_handler(set_packaging, state=FulfillmentForm.packaging)
    dp.register_message_handler(set_box_quantity, state=FulfillmentForm.box_quantity)
    dp.register_callback_query_handler(
        set_packaging_size, state=FulfillmentForm.packaging_size
    )
    dp.register_callback_query_handler(set_tagging, state=FulfillmentForm.tagging)
    dp.register_callback_query_handler(set_inserts, state=FulfillmentForm.inserts)
    dp.register_callback_query_handler(set_warehouse, state=FulfillmentForm.warehouse)
