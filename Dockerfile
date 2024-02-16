FROM python:3.11-slim

WORKDIR /online-mart

COPY requirements.txt /online-mart

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_RUN_PORT 5000
ENV FLASK_RUN_HOST 0.0.0.0

EXPOSE 5000

CMD ["flask", "run"]
