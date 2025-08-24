import nest_asyncio
nest_asyncio.apply()
import asyncio
import logging
from function import create_table
from initialization import bot, dp

logging.basicConfig(level=logging.INFO)

DB_NAME = 'quiz_bot.db'
DICT_DATA= 'data.json'

async def main():
    await create_table()
    await dp.start_polling(bot)
if __name__ == "__main__":
    asyncio.run(main())