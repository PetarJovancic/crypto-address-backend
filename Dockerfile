FROM python:3.9-slim-buster

# # set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt
COPY ./ ./

WORKDIR /usr/src/app 
# EXPOSE 5000
CMD ["sh", "-c", "sleep 2 \ 
    && python -m flask run --host=0.0.0.0"]