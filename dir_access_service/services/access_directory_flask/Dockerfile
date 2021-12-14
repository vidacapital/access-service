# base image
FROM python:3.7.3-slim-stretch

RUN apt-get update && apt-get install -y netcat

RUN pip install --upgrade pip

# set working directory
WORKDIR /usr/src/app

# add and install requirements
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install gunicorn==19.9.0

# add entrypoint.sh
COPY ./entrypoint.sh /usr/src/app/entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh

ENV PYTHONUNBUFFERED 1

# add app
COPY . /usr/src/app

# run server
CMD ["/usr/src/app/entrypoint.sh"]