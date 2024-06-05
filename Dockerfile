FROM python:3.12.3-bookworm

WORKDIR  /app

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 10000

CMD [ "python", "src/main.py" ]
