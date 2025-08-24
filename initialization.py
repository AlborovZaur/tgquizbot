from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Router

router = Router()

API_TOKEN = '8246639574:AAEfrgxFmjeuc6BSnQsn92NC9epeB3k8vOs'
bot = Bot(token=API_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

dp.include_router(router)