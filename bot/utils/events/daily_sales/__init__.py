from datetime import datetime, timedelta
from json import load
import random

from aiogram.types import InputFile
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from ....logs import logger

from ....database.methods.goods import update as goods_update

scheduler = AsyncIOScheduler(timezone="Europe/Moscow")

from .... import config

CHANNEL_ID = -1001966002567


def get_sale(sale_name: str) -> dict:
    with open(f"bot/utils/events/daily_sales/sales/{sale_name}/properties.json") as props_json:
        sale = {
            "settings": load(props_json)['settings'],
            "preview": f"bot/utils/events/daily_sales/sales/{sale_name}/preview.png"
        }

    return sale


def get_random_sale() -> str:
    with open("bot/utils/events/daily_sales/sales/config.json") as sales_config:
        config_json = load(sales_config)

    return f"sale{random.randint(1, config_json['amount'])}"


async def post_sale(bot):
    sale = get_sale(get_random_sale())
    photo = InputFile(sale['preview'])

    for discount in sale['settings']['discounts']:
        await goods_update.update(discount['good_id'], 'discount_id', discount['discount_amount'])
        logger.info(
            f"[Таверна скидок] Обновлена скидка на товар №{discount['good_id']} до {discount['discount_amount']} руб.")

    await bot.send_photo(chat_id=CHANNEL_ID,
                         caption='👀 Таверна скидка — это ваша возможность приобрести давно желаемую игру или подписку со скидкой. Предложения меняются ежедневно.\n\n<a href="https://t.me/portablemarket_bot">▶ Перейти в магазин</a>',
                         parse_mode="HTML",
                         photo=photo)


scheduler.add_job(post_sale, trigger="cron", hour=10, minute=0,
                  kwargs={'bot': config.get_bot()})
scheduler.start()
