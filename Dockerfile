FROM rapidfort/flaskapp:latest

RUN mkdir /application/modules

COPY modules/SnapCrap.py /application/modules/SnapCrap.py

COPY requirements.txt /application/requirements2.txt

RUN pip3 install -r /application/requirements2.txt

COPY main.py /application/flask_app.py