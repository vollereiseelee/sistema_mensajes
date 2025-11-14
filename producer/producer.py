import pika
import json
import time
import random

def connect_rabbitmq():
    while True:
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
            return connection
        except:
            print("Esperando RabbitMQ...")
            time.sleep(3)

connection = connect_rabbitmq()
channel = connection.channel()

channel.exchange_declare(exchange='weather', exchange_type='direct', durable=True)

while True:
    data = {
        "station_id": "STATION-001",
        "temperature": round(random.uniform(-5, 40), 2),
        "humidity": round(random.uniform(10, 90), 2),
        "pressure": round(random.uniform(900, 1100), 2)
    }

    message = json.dumps(data)
    channel.basic_publish(
        exchange='weather',
        routing_key='weather_key',
        body=message,
        properties=pika.BasicProperties(delivery_mode=2)
    )
    print(f"Publicado: {message}")
    time.sleep(5)
