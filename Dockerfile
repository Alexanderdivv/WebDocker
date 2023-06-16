FROM python:3.9-slim

RUN pip install flask pytz gunicorn mysql-connector-python pybase64 pillow

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

# COPY app.py /

CMD ["python", "app.py"]

# CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app