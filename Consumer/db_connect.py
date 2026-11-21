import psycopg2
import time
import os


def db_connection():
    retries = 10
    for i in range(retries):
        try:
            conn = psycopg2.connect(
                host=os.getenv("DB_HOST"),
                database=os.getenv("DB_NAME"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD")
            )
            print("✅ Connected to postgres")
            return conn
        
        except Exception as e:
                print(f"⏳ Postgres not ready, retrying in 3s... ({i+1}/{retries})")
                time.sleep(3)
    raise Exception("❌ Could not connect to postgres after retries")

def insert_event(event, cursor):
    query = """
    INSERT INTO events(
         player_id,
         session_id,
         timestamp,
         heart_rate,
         distance,
         acceleration,
         speed,
         calories   
    )
    VALUES(%s,%s,%s,%s,%s,%s,%s,%s)
    """
    cursor.execute(query,(
                   event["player_id"],
                   event["session_id"],
                   event["timestamp"],
                   event["heart_rate"],
                   event["distance"],
                   event["acceleration"],
                   event["speed"],
                   event["calories"])
                   )
    