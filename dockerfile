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

COPY . /app
WORKDIR /app

RUN pip3 install -r requirements.txt

RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.29.1/geckodriver-v0.29.1-linux64.tar.gz && \
	tar xf geckodriver-v0.29.1-linux64.tar.gz && \
	chmod +x geckodriver && \
	mv geckodriver /usr/local/bin && \
	rm geckodriver-v0.29.1-linux64.tar.gz

#RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py -o /tmp/install-poetry.py && \
#	python /tmp/install-poetry.py -y && \
#	export PATH="$HOME/.local/bin:$PATH" && \
#	poetry install --no-dev

CMD ["uvicorn", "newsbotWorkerApi.app:app", "--host", "0.0.0.0", "--port", "8001"]