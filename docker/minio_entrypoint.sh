#!/bin/sh
set -e

# Start the MinIO server in the background
/usr/bin/minio server /data --console-address ":9001" &

# Sleep for a few seconds to allow MinIO to start
sleep 5  # Adjust this value as needed depending on startup time

# Define bucket names
BUCKET1="bucket1"
BUCKET2="bucket2"

# Create bucket if not exists
create_bucket_if_not_exists() {
  bucket=$1
  if ! /usr/bin/mc ls minio/$bucket >/dev/null 2>&1; then
    echo "Bucket '$bucket' does not exist, creating it."
    /usr/bin/mc mb minio/$bucket
  else
    echo "Bucket '$bucket' already exists."
  fi
}

# Setup MinIO client (mc)
mc alias set minio http://127.0.0.1:9000 "$MINIO_ROOT_USER" "$MINIO_ROOT_PASSWORD"

# Check and create buckets
create_bucket_if_not_exists $BUCKET1
create_bucket_if_not_exists $BUCKET2

# Bring the MinIO server to the foreground to keep the container running
wait
