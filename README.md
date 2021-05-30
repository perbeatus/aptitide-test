# Aptitude test

Simple app created for job interview.

# How-To

## Requirements
  - Docker

## Start stack 

```bash
# Navigate to app folder with docker-compose.yaml file
$ cd path/to/folder/with/app

# run docker stack with
$ DB_PASSWORD="any-db-password" docker compose up --build
```

Successful app run will yield `audit-result.md` file.

## Stop stack

After execution finished press Ctrl+c and execute
```bash
$ docker compose down
```
Remnove containers, network and mounts.
