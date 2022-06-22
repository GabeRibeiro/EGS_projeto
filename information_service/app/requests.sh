#!/bin/sh
echo "Waiting for database to be up..."

echo "" | nc -w 1  information-service-db 3306

while [ ! $? -eq 0 ]; do
    sleep 1
    echo "" | nc -w 1  information-service-db 3306
done
sleep 5
echo -e "\nDatabase up..."
sleep 5
echo -e "Starting app..."

python3 make_requests.py
