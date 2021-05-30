FROM python:3.7-slim-buster
COPY . /movies-audit/
WORKDIR /movies-audit/
RUN ["python3", "-m", "pip", "install", "-r", "requirements.txt"]
ENTRYPOINT [ "python3", "main.py" ]