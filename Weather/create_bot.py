from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
import config
import logging
storage = MemoryStorage()
logging.basicConfig(level=logging.INFO)
bot = Bot(token=config.token)
dp = Dispatcher()