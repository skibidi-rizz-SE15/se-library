#!/bin/bash

# Function to test database connection
check_db_connection() {
    echo "Testing database connection..."
    python test_db_connection.py
    return $?
}

# Function to wait for database
wait_for_db() {
    local retries=30
    local wait_time=2

    for i in $(seq 1 $retries); do
        check_db_connection
        if [ $? -eq 0 ]; then
            echo "Database is ready!"
            return 0
        fi
        echo "Attempt $i/$retries: Database not ready yet. Waiting ${wait_time} seconds..."
        sleep $wait_time
    done

    echo "Could not connect to database after $retries attempts"
    return 1
}

# Main execution
echo "Starting initialization process..."

# Wait for database to be ready
wait_for_db
if [ $? -ne 0 ]; then
    exit 1
fi

# Run database migrations
echo "Running database migrations..."
reflex db migrate

# Start the application
echo "Starting the application..."
exec reflex run --env prod --backend-only --loglevel debug