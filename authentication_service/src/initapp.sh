#!/bin/sh
echo "Waiting for database to be up and running"

echo "" | nc -w 1  authratecheck-db 27017

while [ ! $? -eq 0 ]; do
    sleep 2
    echo "" | nc -w 1  authratecheck-db 27017
done
sleep 10
echo -e "\n Database is up..."
sleep 10
echo -e "\n Starting app..."

npm start 