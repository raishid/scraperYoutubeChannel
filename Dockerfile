FROM tiangolo/uwsgi-nginx-flask:python3.9

RUN apt update && apt install -y unzip xvfb libxi6 libgconf-2-4 wget curl
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list'
RUN apt update && apt install -y google-chrome-stable

COPY ./requirements.txt /tmp/

RUN pip3 install --no-cache-dir -r /tmp/requirements.txt

RUN mkdir -p /usr/src/app

COPY . /usr/src/app

WORKDIR /usr/src/app

EXPOSE 5000

CMD ["gunicorn", "--conf", "/usr/src/app/gunicorn_conf.py", "--bind", "0.0.0.0:5000", "wsgi:application"]