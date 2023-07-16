from aiogram import Dispatcher

from json import loads

from bot.handlers.user import start, product_catalog, category_view, good_view, create_order


def setup(dp: Dispatcher):
    dp.register_message_handler(start.start, commands=["start"])
    dp.register_message_handler(product_catalog.product_catalog, text="Каталог товаров 🛒")
    dp.register_callback_query_handler(category_view.category_view, lambda clb: str(clb.data).startswith("category_"))
    dp.register_callback_query_handler(good_view.good_view, lambda clb: str(clb.data).startswith("good_"))
    dp.register_callback_query_handler(create_order.create_order, lambda clb: str(clb.data).startswith('create_order_'))