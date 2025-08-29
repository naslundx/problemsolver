# backend

## db creation
```sh
createdb marcus.naslund
createuser marcus2 -s -W  # superuser, with password prompt
```
or with psql
```sh
CREATE USER myuser WITH PASSWORD 'mypassword';
CREATE DATABASE mydb OWNER myuser;
GRANT ALL PRIVILEGES ON DATABASE mydb TO myuser;
```

and ensure DATABASE_URL is set in .venv or env

## db setup
see reset-database.sh script

## dev
```sh
uv venv
source .venv/bin/activate
uv run main.py
```
