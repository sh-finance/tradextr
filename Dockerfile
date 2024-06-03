FROM python:3.12.3-bookworm

WORKDIR  /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 10000

CMD [ "python", "src/main.py" ]
