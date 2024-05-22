# Aplikacje Mobilne - projekt 2023/2024

### How to run it

> *optional*
> 
> `python -m venv venv && source venv/bin/activate`

0. Setup database
- Create user and database from `sql/db1.0.sql`.
- Edit `config.py` to match your setup.

1. Install required requirements
```bash
pip install -r requirements.txt
```
2. Run the app
```bash
cd app
python main.py
```

### How to run it (docker version)

```
docker-compose up
```