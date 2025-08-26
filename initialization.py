from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Router

router = Router()

API_TOKEN = 'Your bot token'
bot = Bot(token=API_TOKEN)
dp = Dispatcher(storage=MemoryStorage())


dp.include_router(router)
