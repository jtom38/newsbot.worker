FROM python:3.9-slim-bullseye
ENV DEBIAN_FRONTEND=noninteractive
RUN echo deb http://deb.debian.org/debian/ unstable main contrib non-free >> /etc/apt/sources.list && \
	apt-get update && export DEBIAN_FRONTEND=noninteractive \
	&& apt-get install -y --fix-missing \
		#git \
		make \
		#curl \
		unzip \
		wget \
		gnupg \
		gnupg2 \
		gnupg1 \
		firefox-esr \
		build-essential \
	&& apt-get autoremove -y \
	&& apt-get clean \
	&& apt-get autoclean

RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.30.0/geckodriver-v0.30.0-linux64.tar.gz && \
	tar xf geckodriver-v0.30.0-linux64.tar.gz && \
	chmod +x geckodriver && \
	mv geckodriver /usr/local/bin && \
	rm geckodriver-v0.30.0-linux64.tar.gz
	
RUN pip3 install poetry
COPY . /app
WORKDIR /app
RUN poetry config virtualenvs.create false && \
		poetry install --no-interaction --no-ansi
CMD ["uvicorn", "workerApi.app:app", "--host", "0.0.0.0", "--port", "8001"]