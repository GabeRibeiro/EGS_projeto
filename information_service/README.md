
API dos DAEMONS para gestão apatir do BackOffice 

1. Crie um virtual environment:
```bash
python3 -m venv venv
```

2. Active o virtual environment (precisa de repetir este passo sempre que começar uma nossa sessão/terminal):
```bash
source venv/bin/activate
```

3. Instale os requisitos:
```bash
pip install -r requirements.txt
```


4. Update requisitos:
```bash
pip-review --auto
```

5. Build & Run Docker:

```bash
sudo docker-compose -f deploy/docker-compose.yml  up --buil
```

6. Run Docker:

```bash
sudo docker-compose -f deploy/docker-compose.yml  up
```