import pika
import json
import time
import random
from prometheus_client import start_http_server, Counter

messages_sent = Counter("weather_messages_sent_total", "Mensajes enviados al exchange de RabbitMQ")
producer_errors = Counter("weather_producer_errors_total", "Errores del producer al enviar mensajes")

def connect_rabbitmq():
    while True:
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
            return connection
        except:
            print("Esperando RabbitMQ...")
            time.sleep(3)


start_http_server(8001)
print("Servidor de métricas del PRODUCER escuchando en :8001")

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
    try:
        channel.basic_publish(
            exchange='weather',
            routing_key='weather_key',
            body=message,
            properties=pika.BasicProperties(delivery_mode=2)
        )
        messages_sent.inc()  # métrica
        print(f"Publicado: {message}")

    except Exception as e:
        print("Error al publicar mensaje:", e)
        producer_errors.inc()

    time.sleep(5)
