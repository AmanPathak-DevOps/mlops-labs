FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN python3 -m pip install --upgrade pip

RUN python3 -m pip install -r requirements.txt

COPY . .

EXPOSE 5001

CMD ["python3", "app.py"]
