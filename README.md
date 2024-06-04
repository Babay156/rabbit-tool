Простая в использовании утилита для проверки, архивации и восстановления сообщений очередей RabbitMQ

1. **требования к установке**
    - Python3
    - pip
    - модуль pika

2. **установка**
    ```
    pip install pika
    ```
3. **использование**

   скачайте утилиту
    ```
    git clone https://github.com/Babay156/rabbit-tool.git
    cd ./rabbit-tool
    ```
    отредактируйте в файле rabbit-tool.py переменные перед запуском:
    ```
    # Параметры соединения по умолчанию
    DEFAULT_SERVER = 'Server_IP'
    DEFAULT_PORT = 25672
    DEFAULT_VIRTUAL_HOST = '/'
    DEFAULT_USER = 'username'
    DEFAULT_PASSWORD = 'password'
    BAK_DIRECTORY = 'BAK'
    QUEUE_NAMES_FILE = 'queue_names.txt'
    ```
    добавьте в файл `queue_names.txt` список очередей выбранного виртуального хоста

    запуск без параметров проверяет корректность подключения и выводит список очередей
    ```
    python rabbit-tool
    ```
    эквивалентный вывод даёт параметр `print`
    ```
    python rabbit-tool print
    ```
5. **допустимые параметры запуска:**

    делает копию сообщений в каталог `./BAK/VIRTUAL_HOST/<имя очереди>`. данная команда очищает очередь
    ```
    python rabbit-tool backup
    ```
    восстанавливает сообщения из каталога `./BAK/VIRTUAL_HOST/<имя очереди>`
    ```
    python rabbit-tool restore
    ```
    отправляет 10 сообщений по 10 случайных символов в очередь
    ```
    python rabbit-tool rnd
    ```
