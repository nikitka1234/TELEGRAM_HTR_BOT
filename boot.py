from create_bot import dp
from aiogram import executor
from handlers import client, admin, other
from handlers import inline_client
from keyboards import history_kb

import logging


# Настраиваем логирование

# Если хотите создать файл с логами - используйте имя файла в basicConfig()
# Пример: filename='project_log.log'
logging.basicConfig(level=logging.INFO)

client.register_handlers_client(dp)
inline_client.register_inline_handlers_client(dp)
history_kb.register_history_kb(dp)


if __name__ == "__main__":
    """
    long polling - поддерживает постоянное подключение к серверу
    """
    # чтобы избежать ошибки 'Updates were skipped successfully' - удалите 'skip_updates=True'
    executor.start_polling(dp, skip_updates=True)
