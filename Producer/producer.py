import random
import time
from confluent_kafka import Producer
import uuid
import json
from datetime import datetime, timedelta

producer = Producer({"bootstrap.servers": "kafka:9092"})

players_id = [
    "11111111-1111-1111-1111-111111111111",
    "22222222-2222-2222-2222-222222222222",
    "33333333-3333-3333-3333-333333333333"
]

session_id = str(uuid.uuid4())

SESSION_DATE = datetime(2026, 4, 25)

current_time = SESSION_DATE


def generate_event(player_id):
    global current_time

    heart_rate = random.randint(90, 180)

    speed = round(random.uniform(5, 30), 2)

    acceleration = round(random.uniform(0, 3.5), 2) #m/s²

    distance = round(random.uniform(0, 1), 2)

    calories = round(random.uniform(8, 12), 2)

    event = {
        "player_id": player_id,
        "session_id": session_id,
        "timestamp": current_time.isoformat(),
        "heart_rate": heart_rate,
        "speed": speed,
        "acceleration": acceleration,
        "distance": distance,
        "calories": calories
    }

    current_time += timedelta(seconds=10)

    return event


def delivery_report(err, msg):
    if err:
        print(f" ERROR: {err}")
    else:
        print(f" Sent: {msg.value().decode('utf-8')}")


print("\n--------------------------------------------------\n")
print(f"Starting simulation for date: {SESSION_DATE.date()}\n")

try:
    while True:
        for player_id in players_id:
            event = generate_event(player_id)
            value = json.dumps(event).encode("utf-8")

            producer.produce(
                topic="players_stats_raw",
                value=value,
                callback=delivery_report,
            )

        producer.poll(0)
        time.sleep(2)

except KeyboardInterrupt:
    print(" Stopping producer...")

finally:
    producer.flush()