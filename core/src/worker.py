import os
import json
import time
import psycopg2
import redis
from datetime import datetime
from psycopg2.extras import execute_values
import time
from dotenv import load_dotenv

load_dotenv()

REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = int(os.getenv("REDIS_PORT")) # type: ignore
REDIS_DB = int(os.getenv("REDIS_DB")) # type: ignore


POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = int(os.getenv("POSTGRES_PORT")) # type: ignore
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")

REDIS_LIST_NAME = "pending_to_save"

BATCH_HOLD_SECONDS = 5 * 1  # 5 minutes


def connect_redis():
    return redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True)


def connect_postgres():
    return psycopg2.connect(
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
        dbname=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
    )


def bulk_insert_messages(cursor, messages):
    insert_query = """
        INSERT INTO messages (sender_id, receiver_id, content, sent_at, status, delivered_at)
        VALUES %s
    """
    # Prepare data tuples for execute_values
    data_tuples = [
        (
            msg["sender_id"],
            msg["receiver_id"],
            msg["content"],
            msg["sent_at"],
            msg["status"],
            datetime.utcnow(),  # delivered_at is current time when inserted
        )
        for msg in messages
    ]
    from psycopg2.extras import execute_values

    execute_values(cursor, insert_query, data_tuples)


def run_worker():
    print("Starting Redis -> PostgreSQL batch worker with 5 minute hold...")
    redis_client = connect_redis()

    batch_messages = []
    batch_start_time = datetime.utcnow()

    while True:
        try:
            with connect_postgres() as conn:
                with conn.cursor() as cursor:
                    while True:
                        # BLPOP with 1 second timeout (returns None if timeout)
                        popped = redis_client.blpop(REDIS_LIST_NAME, timeout=1)
                        if popped:
                            _, msg_json = popped
                            print(f"Received message: {msg_json}")

                            try:
                                message_data = json.loads(msg_json)

                                # Parse or default sent_at
                                if "sent_at" in message_data:
                                    if isinstance(message_data["sent_at"], str):
                                        message_data["sent_at"] = datetime.fromisoformat(message_data["sent_at"])
                                else:
                                    message_data["sent_at"] = datetime.utcnow()

                                batch_messages.append(message_data)
                            except (json.JSONDecodeError, KeyError) as e:
                                print(f"Failed to parse or missing fields in message: {e}")
                            except Exception as e:
                                print(f"Unexpected error parsing message: {e}")

                        # Check if batch hold time expired or if batch has messages older than 5 mins
                        now = datetime.utcnow()
                        elapsed = (now - batch_start_time).total_seconds()

                        if elapsed >= BATCH_HOLD_SECONDS and batch_messages:
                            print(f"Batch hold time reached. Saving {len(batch_messages)} messages to DB...")
                            try:
                                bulk_insert_messages(cursor, batch_messages)
                                conn.commit()
                                print("Batch saved to DB.")
                                batch_messages.clear()
                                batch_start_time = datetime.utcnow()
                            except Exception as e:
                                print(f"Failed to save batch to DB: {e}")
                                # Optional: decide what to do with unsaved batch (retry, discard, etc.)

        except (psycopg2.OperationalError, redis.exceptions.ConnectionError) as e:
            print(f"Connection error: {e}, retrying in 5 seconds...")
            time.sleep(5)
        except Exception as e:
            print(f"Unexpected error: {e}, continuing...")


if __name__ == "__main__":
    run_worker()