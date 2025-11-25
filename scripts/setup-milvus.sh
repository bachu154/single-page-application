#!/bin/bash

echo "Setting up Milvus Vector Database..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Milvus container already exists
if docker ps -a --format '{{.Names}}' | grep -q '^milvus$'; then
    echo "Milvus container already exists. Removing it..."
    docker rm -f milvus
fi

# Pull latest Milvus image
echo "Pulling Milvus image..."
docker pull milvusdb/milvus:latest

# Run Milvus container
echo "Starting Milvus container..."
docker run -d --name milvus \
  -p 19530:19530 \
  -p 9091:9091 \
  milvusdb/milvus:latest

# Wait for Milvus to start
echo "Waiting for Milvus to start (30 seconds)..."
sleep 30

# Check if Milvus is running
if docker ps --format '{{.Names}}' | grep -q '^milvus$'; then
    echo "✓ Milvus is running successfully!"
    echo "  - gRPC endpoint: localhost:19530"
    echo "  - Web UI: http://localhost:9091"
else
    echo "✗ Failed to start Milvus. Check logs with: docker logs milvus"
    exit 1
fi

echo "Setup complete!"
