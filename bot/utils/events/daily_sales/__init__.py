from json import load
import random

from aiogram.types import InputFile
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from ....logs import logger

from ....database.methods.goods import update as goods_update

from .... import config

# Включен ли ивент
IS_ENABLED = False

EVENT_NAME = "Таверна скидок"

# Определяем часовой пояс, на который будет ориентироваться
# система при публикации ивента
scheduler = AsyncIOScheduler(timezone="Europe/Moscow")

# Указываем канал, в который будет публиковаться ивент
CHANNEL_ID = -1001966002567

# Путь до папки с содержимом картинок и config содержимого ивента
PATH = "bot/utils/events/daily_sales/sales/"


def get_sale(sale_name: str) -> dict:
    with open(f"{PATH}/{sale_name}/properties.json") as props_json:
        sale = {
            "settings": load(props_json)['settings'],
            "preview": f"{PATH}/{sale_name}/preview.png"
        }

    return sale


def get_random_sale() -> str:
    with open(f"{PATH}/config.json") as sales_config:
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
                         caption=f'👀 Таверна скидок — это ваша возможность приобрести давно желаемую игру или подписку со скидкой. Предложения меняются ежедневно.\n\n<a href="{config.SHOP_BOT_URL}">▶ Перейти в магазин</a>',
                         parse_mode="HTML",
                         photo=photo)


if IS_ENABLED:
    scheduler.add_job(post_sale, trigger="cron", hour=10, minute=10,
                      kwargs={'bot': config.get_bot()})
    scheduler.start()
else:
    logger.info(
        f"Ивент [{EVENT_NAME}] отключен в настройках. Перейдите в __init__ и поменяйте IS_ENABLED на true для включения.")
