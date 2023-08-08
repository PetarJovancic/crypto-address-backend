FROM python:3.9

RUN python3 -m pip install flask
RUN mkdir /app
WORKDIR /app

COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./ ./
ENV FLASK_APP=run.py

CMD ["sh", "-c", "sleep 5 \ 
    && python -m flask run --host=0.0.0.0"]