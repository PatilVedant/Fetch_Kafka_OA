from confluent_kafka import Consumer, Producer, KafkaError # type: ignore
import json
import logging

# Configure logging instead of print for better performance
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Kafka configuration for the consumer
consumer_conf = {
    'bootstrap.servers': 'localhost:29092',
    'group.id': 'my-group',
    'auto.offset.reset': 'earliest'
}
# Kafka configuration for the producer
producer_conf = {
    'bootstrap.servers': 'localhost:29092'
}
# Create consumer and producer instances
consumer = Consumer(consumer_conf)
producer = Producer(producer_conf)

# Subscribe to the 'user-login' topic
consumer.subscribe(['user-login'])

def process_message(message):
    #Process the Kafka message by transforming 'device_type' to uppercase.
    try:
        # Decode the JSON message
        data = json.loads(message.value().decode('utf-8'))
    except json.JSONDecodeError as e:
        # Log JSON decoding errors
        logger.error(f"Error decoding JSON: {e}")
        data = {}  # Initialize with an empty dictionary if JSON decoding fails

    # Check if 'device_type' key exists and transform it to uppercase
    if 'device_type' in data:
        data['device_type'] = data['device_type'].upper()
    else:
        # Log a warning if 'device_type' key is not found
        logger.warning(f"'device_type' key not found in message: {data}")

    # Return the processed message as a JSON string
    return json.dumps(data).encode('utf-8')

# Set batch size for batch processing to enhance processing 
batch_size = 10
messages = []

try:
    while True:
        # Poll messages from the consumer with a 1-second timeout
        msg = consumer.poll(timeout=1.0)
        if msg is None:
            continue # No message received, continue polling
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                # End of partition event, continue polling
                continue
            else:
                # Log other errors and break the loop
                logger.error(msg.error())
                break

        # Process the received message
        processed_message = process_message(msg)
        messages.append(processed_message)

        # If the batch size is reached, send the messages
        if len(messages) >= batch_size:
            for message in messages:
                producer.produce('processed-user-login', message)
            producer.flush() # Ensure all messages are sent
            messages = [] # Clear the batch
except KeyboardInterrupt:
    pass
finally:
    # Send any remaining messages
    if messages:
        for message in messages:
            producer.produce('processed-user-login', message)
        producer.flush() # Ensure all messages are sent

      # Close the consumer
    consumer.close()
