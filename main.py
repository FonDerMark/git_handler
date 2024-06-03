import json
import pika
import threading
from plyer import notification


# Функция для отправки уведомления
def show_notification(version):
    notification.notify(
        title="Version Update",
        message=f"New Version: {version}",
        timeout=10  # Время отображения уведомления в секундах
    )


# Функция для прослушивания RabbitMQ
def listen_to_rabbitmq():
    def callback(ch, method, properties, body):
        data = json.loads(body)
        print("Received %r" % data)
        show_notification(data['version'])

    credentials = pika.PlainCredentials('test', 'test')
    connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.0.166', credentials=credentials))
    channel = connection.channel()

    channel.queue_declare(queue='version_queue')
    channel.basic_consume(queue='version_queue', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


# Основная функция
def main():
    # Запуск слушателя RabbitMQ в отдельном потоке
    rabbitmq_thread = threading.Thread(target=listen_to_rabbitmq)
    rabbitmq_thread.start()
    rabbitmq_thread.join()


if __name__ == "__main__":
    main()
