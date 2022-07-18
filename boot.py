from create_bot import dp
from aiogram import executor
from handlers import client, admin, other
from handlers import fsm_client

import logging


# Настраиваем логирование

# Если хотите создать файл с логами - используйте имя файла в basicConfig()
# Пример: filename='project_log.log'
logging.basicConfig(level=logging.INFO)


client.register_handlers_client(dp)
fsm_client.register_handlers_photo(dp)
fsm_client.register_handlers_common(dp)


if __name__ == "__main__":
    """
    long polling - поддерживает постоянное подключение к серверу
    """
    # чтобы избежать ошибки 'Updates were skipped successfully' - удалите 'skip_updates=True'
    executor.start_polling(dp, skip_updates=True)
