from confluent_kafka import Consumer
import json
from db_connect import db_connection , insert_event

consumer = Consumer({
    "bootstrap.servers":"kafka:9092",
    "group.id":"tracker_1",
    "auto.offset.reset":"earliest"
})

conn = db_connection()
cursor = conn.cursor()


consumer.subscribe(["players_stats_raw"])

print("consumer is fetching for data")

try:
    while True:
        msg = consumer.poll(1)

        if msg is None:
            continue

        if msg.error():
            print(f"❌ Error: {msg.error()}")
            continue

        try:
            value = msg.value().decode("utf-8")
            stats = json.loads(value)
            insert_event(stats,cursor)
            conn.commit()
            print("✅ event added succedfully")

        except Exception as e:
            print(f" ❌ Invalid message: {e}")
            continue


except KeyboardInterrupt:
    print("Stopping consumer...")

finally:
    consumer.close()

