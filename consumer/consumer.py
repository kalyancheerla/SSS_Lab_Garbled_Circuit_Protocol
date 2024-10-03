from kafka import KafkaConsumer
import logging
import argparse

logging.basicConfig(level=logging.INFO)

class Consumer:
    def __init__(self, host, topic):
        self.kafka_host = host
        self.kafka_topic = topic
        self.consumer = KafkaConsumer(
            self.kafka_topic,
            bootstrap_servers=self.kafka_host,
        )

    def consume_from_kafka(self):
        for message in self.consumer:
            logging.info(message.value)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Kafka Consumer with command-line arguments.')

    # Define command-line arguments
    parser.add_argument('broker', type=str, help='The Kafka broker address (e.g., localhost:9092)')
    parser.add_argument('topic', type=str, help='The Kafka topic to send messages to (e.g., chatmsgs)')

    # Parse the arguments
    args = parser.parse_args()

    # Create the producer using the parsed arguments
    consumer = Consumer(args.broker, args.topic)
    while True:
        consumer.consume_from_kafka()
