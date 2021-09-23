FROM python:3.9-slim-bullseye
ENV DEBIAN_FRONTEND=noninteractive
RUN echo deb http://deb.debian.org/debian/ unstable main contrib non-free >> /etc/apt/sources.list && \
	apt-get update && export DEBIAN_FRONTEND=noninteractive \
	&& apt-get install -y --fix-missing \
		git \
		make \
		curl \
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

run wget https://github.com/crate-ci/typos/releases/download/v1.0.3/typos-v1.0.3-x86_64-unknown-linux-gnu.tar.gz && \
	tar xf typos-v1.0.3-x86_64-unknown-linux-gnu.tar.gz && \
	chmod +x typos && \
	mv typos /usr/local/bin && \
	rm typos-v1.0.3-x86_64-unknown-linux-gnu.tar.gz

CMD [ "python", "app.py" ]