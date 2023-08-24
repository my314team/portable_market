from loguru import logger

logger.add("bot/logs/debug.log", format="{time} {level} {message}", level="DEBUG", rotation="100 KB", compression="zip")
