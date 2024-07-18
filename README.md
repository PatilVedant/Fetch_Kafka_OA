# Fetch_Kafka_OA

# Kafka Data Pipeline

## Overview

This assignment sets up a Kafka-based data pipeline to process real-time streaming data. The pipeline consumes messages from a Kafka topic, processes the data, and produces the processed data to another Kafka topic. This setup uses Docker to run Kafka and related services, and Python for the data processing script.

## Prerequisites

- Docker and Docker Compose installed on your local machine.
- Python 3.8+ installed on your local machine.
- Git installed on your local machine.

## Project Structure

├── consumer_producer.py # Python script for consuming and producing Kafka messages
├── docker-compose.yml # Docker Compose file for setting up Kafka and related services
├── Version Check # To check if Kafka is installed or not on your local machine
├── README.md # This readme file


## Setup Instructions

### Step 1: Clone the Repository

```bash
git clone https://github.com/PatilVedant/Fetch_Kafka_OA.git
cd <repo-directory>

### Step 2: Start Docker Containers
Ensure Docker is installed and running. Use the following command to start the Kafka and Zookeeper services:


