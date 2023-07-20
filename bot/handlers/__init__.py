from aiogram import Dispatcher

from json import loads

from bot.handlers.user import start, product_catalog, category_view, good_view, create_order, sales, faq


def setup(dp: Dispatcher):
    dp.register_message_handler(start.start, commands=["start"])
    dp.register_message_handler(product_catalog.product_catalog, text="Каталог товаров 🛒")
    dp.register_message_handler(sales.sales, text="Акции/Скидки 💰")
    dp.register_message_handler(faq.faq, text="Вопрос-Ответ 🔍")

    dp.register_callback_query_handler(faq.how_to_order, lambda clb: str(clb.data).startswith("qa_how_to_order"))
    dp.register_callback_query_handler(faq.good_not_found, lambda clb: str(clb.data).startswith("qa_good_not_found"))
    dp.register_callback_query_handler(faq.how_to_use_promo, lambda clb: str(clb.data).startswith("qa_how_to_use_promo"))
    dp.register_callback_query_handler(faq.payment_not_work, lambda clb: str(clb.data).startswith("qa_payment_not_work"))
    dp.register_callback_query_handler(faq.no_money_sent, lambda clb: str(clb.data).startswith("qa_no_money_sent"))
    dp.register_callback_query_handler(faq.bot_off, lambda clb: str(clb.data).startswith("qa_bot_off"))

    dp.register_callback_query_handler(create_order.checkpaygood, lambda clb: str(clb.data).startswith("checkpaygood_"))

    dp.register_callback_query_handler(category_view.category_view, lambda clb: str(clb.data).startswith("category_"))
    dp.register_callback_query_handler(good_view.good_view, lambda clb: str(clb.data).startswith("good_"))
    dp.register_callback_query_handler(create_order.create_order, lambda clb: str(clb.data).startswith('create_order_'))
