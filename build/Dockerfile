FROM python:3.6.9
WORKDIR /app
COPY requirements.txt /app
RUN pip install -r requirements.txt
ADD . /app
CMD [ "python", "app.py" ]