ARG PORT

# Use the official lightweight Python image.
# https://hub.docker.com/_/python
# FROM tiangolo/uvicorn-gunicorn:python3.7
FROM python:3.7

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME

# Install production dependencies.
COPY ./requirements.txt .
RUN pip3 install -r requirements.txt

# Download the model
RUN wget https://grammarly-nlp-data-public.s3.amazonaws.com/gector/bert_0_gector.th
# COPY ./bert_0_gector.th .

# Now copy model files
ADD ./gector ./gector
ADD ./data ./data
ADD ./utils ./utils

# The bootstrap script will download the model file into the container image
COPY ./bootstrap.py .
RUN python bootstrap.py

# Now copy the app
COPY ./main.py .

# Run the web service on container startup. Here we use gunicorn
# CMD exec gunicorn -k uvicorn.workers.UvicornWorker --bind :$PORT --workers 1 --threads 1 --timeout 0 main:app
CMD exec gunicorn --bind :$PORT --workers 1 --worker-class uvicorn.workers.UvicornWorker --threads 8 main:app --timeout 0