ARG PORT

# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM tiangolo/uvicorn-gunicorn:python3.7

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

# Now copy model files
COPY ./gector .
COPY ./data .

# Now copy the app
COPY ./main.py .
# COPY ./models.py .

# Run the web service on container startup. Here we use gunicorn
# CMD exec gunicorn -k uvicorn.workers.UvicornWorker --bind :$PORT --workers 1 --threads 1 --timeout 0 main:app
