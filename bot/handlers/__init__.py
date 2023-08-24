from aiogram import Dispatcher

from bot.handlers.user import start, product_catalog, category_view, good_view, create_order, about, faq
from bot.handlers.admin import orders as admin_orders
from bot.handlers.partners import stats_menu as partners_stats_menu


def setup(dp: Dispatcher):
    dp.register_message_handler(start.start, commands=["start"])
    dp.register_message_handler(product_catalog.product_catalog, text="Каталог товаров 🛒")
    dp.register_message_handler(about.about, text="Акции/Скидки 💰")
    dp.register_message_handler(about.about, text="О магазине")
    dp.register_message_handler(faq.faq, text="Вопрос-Ответ 🔍")
    dp.register_message_handler(faq.reviews, text="Отзывы клиентов 📪")
    dp.register_message_handler(faq.support, text="Поддержка 📝")

    dp.register_callback_query_handler(faq.faq, lambda clb: str(clb.data) == "qa")
    dp.register_callback_query_handler(faq.how_to_order, lambda clb: str(clb.data).startswith("qa_how_to_order"))
    dp.register_callback_query_handler(faq.good_not_found, lambda clb: str(clb.data).startswith("qa_good_not_found"))
    dp.register_callback_query_handler(faq.how_to_use_promo,
                                       lambda clb: str(clb.data).startswith("qa_how_to_use_promo"))
    dp.register_callback_query_handler(faq.payment_not_work,
                                       lambda clb: str(clb.data).startswith("qa_payment_not_work"))
    dp.register_callback_query_handler(faq.no_money_sent, lambda clb: str(clb.data).startswith("qa_no_money_sent"))
    dp.register_callback_query_handler(faq.bot_off, lambda clb: str(clb.data).startswith("qa_bot_off"))

    dp.register_callback_query_handler(create_order.checkpaygood, lambda clb: str(clb.data).startswith("checkpaygood_"))

    dp.register_callback_query_handler(category_view.category_view, lambda clb: str(clb.data).startswith("category_"))
    dp.register_callback_query_handler(good_view.good_view, lambda clb: str(clb.data).startswith("good_"))
    dp.register_callback_query_handler(create_order.create_order, lambda clb: str(clb.data).startswith('create_order_'))

    """Админ-панель"""

    dp.register_message_handler(admin_orders.all_unget_orders, text="ап заказы")
    dp.register_message_handler(admin_orders.give_order, lambda msg: str(msg.text).startswith("ап выдать"))
    dp.register_callback_query_handler(admin_orders.confirm_order,
                                       lambda clb: str(clb.data).startswith('confirmorder_'))
    dp.register_callback_query_handler(admin_orders.bad_order, lambda clb: str(clb.data).startswith('badorder_'))

    """Партнер-панель"""
    dp.register_message_handler(partners_stats_menu.stats_menu, text="пстата")
    dp.register_callback_query_handler(partners_stats_menu.last_sales, lambda clb: str(clb.data) == 'lastpartnersales')

    """Кнопки-назад"""
    dp.register_callback_query_handler(product_catalog.to_categories, lambda clb: str(clb.data) == "to_categories")
