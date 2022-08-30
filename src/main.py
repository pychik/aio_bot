import logging as log
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from config import settings


log.basicConfig(level=log.INFO)  # Initialize bot and dispatcher
bot = Bot(token=settings.API_TOKEN, parse_mode=types.ParseMode.HTML)

storage = RedisStorage2(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
)
dp = Dispatcher(bot, storage=storage)


def start_sql():
    try:
        from storages import conn, cur

        cur.execute("""CREATE TABLE IF NOT EXISTS products(product_id serial primary key,
                                            name VARCHAR (100) UNIQUE,
                                            description text,
                                            photo_id VARCHAR (1000),
                                             file_id VARCHAR (1000),
                                              video_id VARCHAR (1000));""")

        conn.commit()
    except Exception as e:
        print(f"Exception : {e}")


if __name__ == '__main__':
    start_sql()
    from handlers import dp
    executor.start_polling(dp, skip_updates=True)
