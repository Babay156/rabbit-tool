import argparse
import os
import random
import string
import pika

# Параметры соединения по умолчанию
DEFAULT_SERVER = 'Server_IP'
DEFAULT_PORT = 25672
DEFAULT_VIRTUAL_HOST = '/'
DEFAULT_USER = 'username'
DEFAULT_PASSWORD = 'password'
BAK_DIRECTORY = 'BAK'
QUEUE_NAMES_FILE = 'queue_names.txt'

# Парсинг аргументов командной строки
parser = argparse.ArgumentParser(description='Скрипт обработки очередей сообщений в RabbitMQ')
parser.add_argument('action', choices=['backup', 'restore', 'rnd', 'print'], nargs='?', default='print', help='Допустимые аргументы запуска: backup, restore, rnd, print')
args = parser.parse_args()

# Подключение к RabbitMQ
credentials = pika.PlainCredentials(DEFAULT_USER, DEFAULT_PASSWORD)
connection = None
channel = None

def connect_to_rabbitmq(server, port, virtual_host):
    global connection, channel
    connection_params = pika.ConnectionParameters(host=server, port=port, virtual_host=virtual_host, credentials=credentials)
    connection = pika.BlockingConnection(connection_params)
    channel = connection.channel()

# Создание директории, если она не существует
def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def read_queue_names():
    queue_names = {}
    with open(QUEUE_NAMES_FILE, 'r') as file:
        for line in file:
            parts = line.strip().split(':')
            if len(parts) == 2:
                virtual_host, queue_name = parts[0], parts[1]
                queue_names[queue_name] = virtual_host
    return queue_names

def backup_messages(queue_name, virtual_host):
    create_directory(os.path.join(BAK_DIRECTORY, virtual_host))
    messages = []
    method_frame, header_frame, body = channel.basic_get(queue_name)
    while method_frame:
        messages.append(body)
        channel.basic_ack(method_frame.delivery_tag)
        method_frame, header_frame, body = channel.basic_get(queue_name)

    file_name = os.path.join(BAK_DIRECTORY, virtual_host, queue_name)
    with open(file_name, 'w') as f:
        for message in messages:
            f.write(message.decode() + '\n')

def restore_messages(queue_name, virtual_host):
    file_name = os.path.join(BAK_DIRECTORY, virtual_host, queue_name)
    if os.path.exists(file_name):
        with open(file_name, 'r') as f:
            messages = f.readlines()

        for message in messages:
            channel.basic_publish(exchange='', routing_key=queue_name, body=message.strip())
    else:
        print(f"Не найден файл резервной копии для очереди '{queue_name}'")

def generate_random_string(length=10):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def rnd_messages(queue_name, virtual_host, num_messages=10):
    for _ in range(num_messages):
        random_string = generate_random_string()
        channel.basic_publish(exchange='', routing_key=queue_name, body=random_string)

def print_queues():
    queue_names = read_queue_names()
    queues_with_messages = []
    for queue_name, virtual_host in queue_names.items():
        message_count = channel.queue_declare(queue=queue_name, passive=True).method.message_count
        if message_count > 0:
            queues_with_messages.append((queue_name, virtual_host, message_count))

    if queues_with_messages:
        print("Очереди с сообщениями:")
        for queue_info in queues_with_messages:
            print(f"Очередь: {queue_info[0]}, Виртуальный хост: {queue_info[1]}, Сообщений: {queue_info[2]}")
    else:
        print("Сообщения в очередях не найдены")

# Определение действия
if args.action == 'backup':
    queue_names = read_queue_names()
    for queue_name, virtual_host in queue_names.items():
        connect_to_rabbitmq(DEFAULT_SERVER, DEFAULT_PORT, virtual_host)
        backup_messages(queue_name, virtual_host)
        print(f"Сообщения из очереди '{queue_name}' успешно сохранены")
        connection.close()
elif args.action == 'restore':
    queue_names = read_queue_names()
    for queue_name, virtual_host in queue_names.items():
        connect_to_rabbitmq(DEFAULT_SERVER, DEFAULT_PORT, virtual_host)
        restore_messages(queue_name, virtual_host)
        print(f"Сообщения из очереди '{queue_name}' успешно восстановлены")
        connection.close()
elif args.action == 'rnd':
    queue_names = read_queue_names()
    for queue_name, virtual_host in queue_names.items():
        connect_to_rabbitmq(DEFAULT_SERVER, DEFAULT_PORT, virtual_host)
        rnd_messages(queue_name, virtual_host)
        print(f"Случайное сообщение успешно добавлено в очередь '{queue_name}'")
        connection.close()
elif args.action == 'print':
    connect_to_rabbitmq(DEFAULT_SERVER, DEFAULT_PORT, DEFAULT_VIRTUAL_HOST)
    print_queues()
    connection.close()
else:
    print("Некорректный запуск, проверьте параметры")
