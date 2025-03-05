#!/bin/bash
set -e

# Load environment variables
export $(grep -v '^#' /app/.env | xargs)

echo "Waiting for PostgreSQL to be ready..."
sleep 10

# Check if the table exists
PGPASSWORD=$DATABASE_PASSWORD psql -U $DATABASE_USERNAME -d $DATABASE_NAME -h db -c "
CREATE TABLE IF NOT EXISTS web_pages (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255),
    html_content TEXT
);"

# Insert HTML content
PGPASSWORD=$DATABASE_PASSWORD psql -U $DATABASE_USERNAME -d $DATABASE_NAME -h db -c "
INSERT INTO web_pages (title, html_content)
VALUES ('main', '$(cat /app/main.html)')
ON CONFLICT (id) DO NOTHING;"