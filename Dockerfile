FROM python:3.12-slim

WORKDIR /backend

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["sleep", "infinity"]
# flask --app app:create_app run --host=0.0.0.0 --port=5000 --debug
# CMD ["flask", "--app", "app:create_app", "run", "--host=0.0.0.0", "--port=5000", "--debug"]