import pika
import psycopg2
import json
import time

from prometheus_client import start_http_server, Counter

# Métricas
messages_received = Counter("weather_messages_received_total", "Mensajes recibidos desde RabbitMQ")
db_errors = Counter("weather_db_errors_total", "Errores al guardar datos en PostgreSQL")

def connect_postgres():
    while True:
        try:
            return psycopg2.connect(
                host="postgres",
                database="weatherdb",
                user="weather",
                password="weather_pass"
            )
        except:
            print("Esperando PostgreSQL...")
            time.sleep(3)

def connect_rabbitmq():
    while True:
        try:
            connection = pika.BlockingConnection(
                pika.ConnectionParameters('rabbitmq')
            )
            return connection
        except:
            print("Esperando RabbitMQ...")
            time.sleep(3)

def callback(ch, method, properties, body):
    messages_received.inc()  # Métrica

    try:
        data = json.loads(body)
        print(f"Recibido: {data}")

        conn = connect_postgres()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO weather_logs (station_id, temperature, humidity, pressure) VALUES (%s, %s, %s, %s)",
            (data["station_id"], data["temperature"], data["humidity"], data["pressure"])
        )
        conn.commit()
        cur.close()
        conn.close()

    except Exception as e:
        print("Error:", e)
        db_errors.inc()

    ch.basic_ack(delivery_tag=method.delivery_tag)

start_http_server(8000)
print("Servidor de métricas Prometheus escuchando en :8000")

connection = connect_rabbitmq()
channel = connection.channel()
channel.exchange_declare(exchange='weather', exchange_type='direct', durable=True)

queue_name = 'weather_queue'
channel.queue_declare(queue=queue_name, durable=True)
channel.queue_bind(exchange='weather', queue=queue_name, routing_key='weather_key')

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue=queue_name, on_message_callback=callback)

print("Esperando mensajes...")
channel.start_consuming()
