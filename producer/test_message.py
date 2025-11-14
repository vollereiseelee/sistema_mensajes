import pika
import json
import time

def connect_rabbitmq():
    while True:
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
            return connection
        except Exception as e:
            print(f"Esperando RabbitMQ... {e}")
            time.sleep(3)


connection = connect_rabbitmq()
channel = connection.channel()


channel.exchange_declare(exchange='weather', exchange_type='direct', durable=True)


data = {
    "station_id": "STATION-TEST",
    "temperature": 25.5,
    "humidity": 70.2,
    "pressure": 1012.3
}

message = json.dumps(data)

channel.basic_publish(
    exchange='weather',
    routing_key='',
    body=message,
    properties=pika.BasicProperties(
        delivery_mode=2
    )
)

print(f"Mensaje de prueba enviado: {message}")

connection.close()
