from kafka import KafkaProducer
from kafka.errors import KafkaError
import json
import faker, uuid
from datetime import datetime
import logging
import time
import argparse

logging.basicConfig(level=logging.INFO)

class Producer:
    def __init__(self, host, topic):
        self.kafka_host = host
        self.kafka_topic = topic
        self.producer = KafkaProducer(
            bootstrap_servers=self.kafka_host, value_serializer=lambda v: json.dumps(v).encode(),
        )

    def publish_to_kafka(self, message):
        try:
            self.producer.send(self.kafka_topic, message)
            self.producer.flush()
        except KafkaError as ex:
            logging.error(f"Exception {ex}")
        else:
            logging.info(f"Published message {message} into topic {self.kafka_topic}")

def create_fake_message(creds=False):
    f = faker.Faker()

    # Default message
    message_text = f.sentence(nb_words=6)

    # If the flag is set, add credentials to the message text
    if creds:
        username = f.user_name()
        password = f.password()
        message_text = f"Hey, my username is {username} and my password is {password}"

    message = {
        "message_id": str(uuid.uuid4()),
        "sender_id": str(uuid.uuid4()),
        "receiver_id": str(uuid.uuid4()),
        "message_text": message_text,
        "timestamp": datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
        "chat_room_id": str(uuid.uuid4()),
        "metadata": {
            "is_read": f.boolean(),
            "is_deleted": f.boolean()
        }
    }
    return message

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Kafka Producer with command-line arguments.')

    # Define command-line arguments
    parser.add_argument('broker', type=str, help='The Kafka broker address (e.g., localhost:9092)')
    parser.add_argument('topic', type=str, help='The Kafka topic to send messages to (e.g., chatmsgs)')

    # Parse the arguments
    args = parser.parse_args()

    # Create the producer using the parsed arguments
    producer = Producer(args.broker, args.topic)

    for i in range(5):
        if i == 3:
            producer.publish_to_kafka(create_fake_message(creds=True))
        producer.publish_to_kafka(create_fake_message())
        time.sleep(5)
