# rabbit-tool
Простая в использовании утилита для проверки, архивации и восстановления сообщений очередей RabbitMQ

требования к установке
Python3
pip
модуль piko

установка
pip install piko

использование
отредактируйте переменные перед запуском:
DEFAULT_SERVER = 'Server_IP'
DEFAULT_PORT = 25672
DEFAULT_VIRTUAL_HOST = '/'
DEFAULT_USER = 'username'
DEFAULT_PASSWORD = 'password'
BAK_DIRECTORY = 'BAK'
QUEUE_NAMES_FILE = 'queue_names.txt'
