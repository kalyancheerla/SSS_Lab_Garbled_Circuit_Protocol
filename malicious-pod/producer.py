import ssl
from kafka import KafkaProducer


context = ssl.create_default_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE


def producer_create(bootstrap_servers="", client_id="", security_protocol="PLAINTEXT",
                    sasl_mechanism="", sasl_plain_username="",
                    sasl_plain_password="", ssl_context=context):
    producer = KafkaProducer(bootstrap_servers=bootstrap_servers,
                             client_id=client_id,
                             security_protocol=security_protocol,
                             sasl_mechanism=sasl_mechanism,
                             sasl_plain_username=sasl_plain_username,
                             sasl_plain_password=sasl_plain_password,
                             ssl_context=ssl_context
                             )
    return producer


def p_create(thread_name, topic_name, num_of_messages):
    list_of_messages = []
    for j in range(1, num_of_messages):
        thread_name.send(topic_name, b'%d' % j)
        list_of_messages.append(j)
    return list_of_messages
