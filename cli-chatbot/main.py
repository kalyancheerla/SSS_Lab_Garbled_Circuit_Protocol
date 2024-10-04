import json
import sys
import threading
from kafka import KafkaProducer, KafkaConsumer
from faker import Faker
from datetime import datetime, timezone
import multiprocessing

# Set up Faker to generate random data
fake = Faker()
#BROKER_IP = 'localhost:9092'
#BROKER_IP = 'broker:9092'
BROKER_IP = 'kafka-cluster-kafka-bootstrap.kafka-production.svc.cluster.local:9092'
#BROKER_IP = '192.168.4.168:9092'

# Function to generate a JSON object for the chat message
def generate_chat_message(username, message_text, chat_room_id):
    chat_message = {
        "message_id": fake.uuid4(),
        "sender_id": fake.uuid4(),
        "receiver_id": fake.uuid4(),  # In a real app, this could be the ID of the intended recipient
        "username": username,
        "message_text": message_text,
        "timestamp": datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S.%f%z'),  # Convert datetime to string
        "chat_room_id": chat_room_id,
        "metadata": {
            "is_read": False,
            "is_deleted": False
        }
    }
    return chat_message

# Kafka producer function to send messages
def kafka_producer(username, chat_room_id, input_queue):
    producer = KafkaProducer(
            bootstrap_servers=[BROKER_IP],  # Replace with your Kafka broker(s)
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

    while True:
        if input_queue is not None:
            message_text = input_queue.get()
        else:
            message_text = input(f"{username}: ")

        if message_text.lower() == 'exit':
            print(f"{username} is leaving the chat...")
            break

        # Generate a chat message JSON object
        chat_message = generate_chat_message(username, message_text, chat_room_id)

        # Send message to Kafka topic 'chat_room'
        producer.send('chat_room', value=chat_message)
        producer.flush()  # Ensure the message is sent immediately

        print(f"Message sent to Kafka: {json.dumps(chat_message, indent=4)}")

# Kafka consumer function to receive messages
def kafka_consumer(chat_room_id, username):
    # Ensure each user has a unique consumer group by appending their username
    consumer = KafkaConsumer(
        'chat_room',  # Topic to consume from
        bootstrap_servers=[BROKER_IP],  # Replace with your Kafka broker(s)
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id=f'chat_group_{chat_room_id}_{username}',  # Unique group for each user
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )

    print(f"Listening for messages in chat room '{chat_room_id}'...")

    # Continuously listen for messages in the background
    for message in consumer:
        chat_message = message.value
        sender_username = chat_message['username']
        message_text = chat_message['message_text']
        timestamp = chat_message['timestamp']

        # Only print messages sent by others
        if sender_username != username:
            print(f"[{timestamp}] {sender_username}: {message_text}")

# Thread function to run producer and consumer simultaneously
def start_chat_app(username, chat_room_id):
    # Start consumer in a separate thread
    consumer_thread = threading.Thread(target=kafka_consumer, args=(chat_room_id, username), daemon=True)

    # Start the consumer thread first
    consumer_thread.start()

    # Run producer in the main thread (blocking)
    kafka_producer(username, chat_room_id)

def start_chat_app2(username, chat_room_id):
    # Start producer in a separate thread
    producer_thread = threading.Thread(target=kafka_producer, args=(username, chat_room_id, None))

    # Start consumer in a separate thread
    consumer_thread = threading.Thread(target=kafka_consumer, args=(chat_room_id, username))

    # Start both threads
    producer_thread.start()
    consumer_thread.start()

    # Join the threads to ensure they run concurrently
    producer_thread.join()
    consumer_thread.join()

def start_chat_app3(username, chat_room_id):
    input_queue = multiprocessing.Queue()

    # Start producer in a separate process
    producer_process = multiprocessing.Process(target=kafka_producer, args=(username, chat_room_id, input_queue))

    # Start consumer in a separate process
    consumer_process = multiprocessing.Process(target=kafka_consumer, args=(chat_room_id, username))

    # Start both processes
    producer_process.start()
    consumer_process.start()

    # Join the processes to ensure they run concurrently and finish together
    producer_process.join()
    consumer_process.join()

# Entry point of the CLI app
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python cli_chat.py <username> <chat_room_id>")
        sys.exit(1)

    username = sys.argv[1]
    chat_room_id = sys.argv[2]

    start_chat_app2(username, chat_room_id)
    # 3 didn't work in normal scenario either
    # 1 & 2 worked with venv setup

