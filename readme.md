# Sistema de Mensajes 

## Table of Contents
1. [Tech Stack & Tools](#tech-stack--tools)
2. [Description](#description)
3. [Main Features](#main-features)
4. [System Components](#system-components)
5. [Architecture](#architecture)
6. [Metrics & Monitoring](#metrics--monitoring)
7. [Equipo de desarrollo](#Equipo-Desarrollo)

---

## Tech Stack & Tools

- **Python 3.13+** para el desarrollo del productor y consumidor.
- **RabbitMQ** como *message broker* principal.
- **PostgreSQL** para almacenar los mensajes procesados.
- **Prometheus** para recoger métricas del sistema.
- **Grafana** para la visualización de dashboards.
- **Docker & Docker Compose** para orquestación.
- Librerías clave:
  - `pika` (RabbitMQ client)
  - `psycopg2` (PostgreSQL client)
  - `prometheus_client` (exporter de métricas)
  - `requests`, `json`, etc.

---

## Description

Este proyecto implementa un **sistema de mensajería distribuido** basado en un flujo *Producer → RabbitMQ → Consumer → PostgreSQL*, con mecanismos de monitoreo en tiempo real mediante **Prometheus** y visualización en **Grafana**.

El objetivo es simular un flujo continuo de mensajes (sensores, logs, eventos, etc.) que son enviados por el producer, almacenados por el consumer y observados mediante dashboards.

---

## Main Features

- ✔ **Producer** que envía mensajes hacia RabbitMQ.
- ✔ **Consumer** que recibe, procesa y almacena los mensajes en PostgreSQL.
- ✔ **Base de datos** inicializada automáticamente mediante `init.sql`.
- ✔ **Prometheus** recolecta métricas del consumer (mensajes procesados, errores, etc.).
- ✔ **Grafana** presenta dashboards de rendimiento y actividad del sistema.
- ✔ **Infraestructura orquestada completamente con Docker Compose**.
- ✔ **Métricas expuestas en /metrics** listas para Prometheus.

---

## System Components

### Producer (`/producer`)
- Archivo principal: `producer.py`
- Envía mensajes periódicos hacia RabbitMQ.
- Incluye prueba de generación de mensajes: `test_message.py`
- Requisitos en `requirements.txt`
- Construcción mediante `Dockerfile`

### Consumer (`/consumer`)
- Archivo principal: `consumer.py`
- Escucha mensajes desde RabbitMQ.
- Inserta datos en PostgreSQL.
- Expone métricas para Prometheus.
- Incluye `requirements.txt` y `Dockerfile`.

### Base de Datos (`/db`)
- `init.sql` crea tabla(s) inicial(es) para almacenar mensajes.

### Prometheus (`/prometheus`)
- Configuración en `prometheus.yml`
- Define *targets* para el consumer y RabbitMQ.

### Docker Compose
- Maneja:
  - RabbitMQ
  - PostgreSQL
  - Producer
  - Consumer
  - Prometheus
  - Grafana

---

### Clonar el repositorio
git clone https://github.com/vollereiseelee/sistema_mensajes.git

### Architecture
```
sistema-mensajes/
├── consumer/
│ ├── Dockerfile
│ ├── consumer.py
│ ├── requirements.txt
│
├── producer/
│ ├── Dockerfile
│ ├── producer.py
│ ├── requirements.txt
│ ├── test_message.py
│
├── db/
│ ├── init.sql
│
├── prometheus/
│ ├── prometheus.yml
│
├── .env
├── docker-compose.yml
└── README.md
```
### Métricas del consumer
Prometheus captura datos como:

- `messages_processed_total`  
- `messages_per_second`  
- `consumer_memory_usage_bytes`  
- `postgres_insert_errors_total`
## Equipo de Desarrollo
- Sebastian Valencia Montesino  
- Andrés Hernández Viaña  
- William Cuello Haydar  
- Juan Silgado Marrugo  

