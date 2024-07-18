try:
   import confluent_kafka # type: ignore
   print("confluent_kafka is installed and can be imported.")
except ImportError as e:
   print(f"Error: {e}")

