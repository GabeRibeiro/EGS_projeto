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

#python3 api_methods.py
#gunicorn -w 4 "app.api_methods:main()"
#gunicorn -w 4 "api_methods:app"
gunicorn --chdir . api_methods:app -w 2 --threads 2 -b 0.0.0.0:8000