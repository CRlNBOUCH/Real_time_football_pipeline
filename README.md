# Real-Time Football Player Performance Tracking Pipeline

A real-time data engineering pipeline that simulates IoT sensor data from football players, streams performance metrics through Apache Kafka, stores them in PostgreSQL, and makes them available for visualization in Power BI.

The project demonstrates an end-to-end streaming architecture, from event generation to data storage and analytics.

## Architecture

The pipeline consists of four Dockerized services:

1. **Producer (Python)**

   Simulates IoT sensor readings every 10 seconds, generating JSON events containing:
   - Heart rate
   - Speed
   - Acceleration
   - Distance covered
   - Calories burned

   Events are published to the Kafka topic `players_stats_raw`.

2. **Apache Kafka (KRaft Mode)**

   Handles real-time event streaming, operating as both broker and controller without requiring ZooKeeper.

3. **Consumer (Python)**

   Continuously consumes Kafka messages, parses incoming events, and inserts records into PostgreSQL.

   Includes retry logic and transaction handling to improve ingestion reliability.

4. **PostgreSQL**

   Stores player and session performance data. A pre-aggregated SQL view provides session-level metrics directly to Power BI.

## Data Flow

```text
IoT Sensor Simulation
        |
        v
  Python Producer
        |
        v
 Apache Kafka
  (KRaft Mode)
        |
        v
  Python Consumer
        |
        v
   PostgreSQL
        |
        v
  SQL Aggregated View
        |
        v
    Power BI
```

## Dashboard & Analytics

The Power BI dashboard provides a session-level overview of player performance, including:

| Metric | Description |
|---|---|
| Average Heart Rate | Average heart rate during a session |
| Peak Heart Rate | Maximum recorded heart rate |
| Maximum Speed | Highest recorded player speed |
| Maximum Acceleration | Peak acceleration |
| Distance Covered | Total distance run per session |
| Calories Burned | Estimated calories burned per session |

## Technologies

- **Python** – Event simulation and Kafka consumption
- **Apache Kafka** – Real-time event streaming
- **KRaft** – Kafka cluster coordination
- **PostgreSQL** – Relational data storage and SQL aggregation
- **Docker & Docker Compose** – Containerization and service orchestration
- **Power BI** – Performance monitoring and visualization

## Getting Started

### Prerequisites

- Docker
- Docker Compose

### 1. Clone the repository

```bash
git clone https://github.com/CRlNBOUCH/Real_time_football_pipeline.git

cd Real_time_football_pipeline
```

### 2. Start the pipeline

```bash
docker compose up --build
```

This builds and starts the four services, with Kafka and PostgreSQL healthchecks used to control service startup dependencies.

### 3. Monitor the containers

```bash
docker compose ps
```

To inspect service logs:

```bash
docker compose logs -f
```

To stop the pipeline:

```bash
docker compose down
```

To stop the services without removing persistent data volumes:

```bash
docker compose down
```

## Project Structure

```text
Real_time_football_pipeline/
│
├── Producer/
│   └── Dockerfile
│
├── Consumer/
│   └── Dockerfile
│
├── db/
│   └── init.sql
│
├── docker-compose.yaml
└── requirements.txt
```

## Engineering Considerations

Beyond implementing the streaming architecture, the project focuses on operational reliability:

- **Service orchestration:** Docker Compose manages the lifecycle and dependencies of the pipeline components.
- **Healthchecks:** Kafka and PostgreSQL readiness checks help prevent premature service startup.
- **Data persistence:** Docker volumes preserve Kafka and PostgreSQL data across container restarts.
- **Error handling:** Consumer-side retry logic and transaction management improve ingestion resilience.
- **Decoupled architecture:** Kafka separates event production from consumption, allowing components to operate independently.

## Data Disclaimer

All player performance readings are simulated using Python. No physical IoT devices or real-time athlete sensors were involved.

The project focuses on the engineering aspects of real-time data ingestion, streaming, storage, and analytics.

---

**Topics:** Data Engineering · Stream Processing · Apache Kafka · Docker · PostgreSQL · Python · Power BI