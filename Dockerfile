FROM rapidfort/flaskapp:latest

COPY requirements.txt /application/requirements2.txt

RUN pip3 install -r /application/requirements2.txt

COPY main.py /application/flask_app.py