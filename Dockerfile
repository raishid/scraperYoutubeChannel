FROM python:3.11-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
	PYTHONUNBUFFERED=1 \
	PIP_NO_CACHE_DIR=1 \
	PLAYWRIGHT_BROWSERS_PATH=/ms-playwright

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
	ca-certificates \
	curl \
	gnupg \
	unzip \
	xvfb \
	libxi6 \
	libgconf-2-4 \
	wget \
	fonts-liberation \
	libnss3 \
	libxss1 \
	libasound2 \
	libatk-bridge2.0-0 \
	libgtk-3-0 && \
	mkdir -p /etc/apt/keyrings && \
	curl -fsSL https://dl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /etc/apt/keyrings/google-chrome.gpg && \
	echo "deb [arch=amd64 signed-by=/etc/apt/keyrings/google-chrome.gpg] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list && \
	apt-get update && apt-get install -y --no-install-recommends google-chrome-stable && \
	rm -rf /var/lib/apt/lists/*

COPY requirements.txt /tmp/requirements.txt

RUN python -m pip install --upgrade pip setuptools wheel && \
	pip install -r /tmp/requirements.txt && \
	python -m playwright install --with-deps chromium

COPY . /app

EXPOSE 5000

CMD ["gunicorn", "--config", "/app/gunicorn_conf.py", "wsgi:application"]