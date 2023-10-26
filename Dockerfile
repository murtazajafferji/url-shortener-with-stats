FROM python:3.10

ENV HOST 0.0.0.0
ENV PORT 8080

COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt
COPY run.py /app/run.py
COPY src /app/src/

WORKDIR /app

RUN echo "Initializing SQLite database..." && python -m src.db.setup

ENTRYPOINT [ "python", "-m", "run" ]