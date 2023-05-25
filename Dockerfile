FROM ubuntu:20.04

MAINTAINER Toan <pdminhtoan@gmail.com>

# Setup environments
ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Ho_Chi_Minh

RUN apt-get update && apt-get install -y --no-install-recommends curl gnupg locales git apt-utils && \
  apt-get -y install --no-install-recommends python3 python3-pip python3-dev build-essential && \
  apt -y install make cmake gcc g++ && \
  apt -y install libsndfile1-dev && \ 
  apt-get -y install libgl1 && \ 
  apt-get -y install poppler-utils && \
  apt install -y tesseract-ocr && \
  pip install --upgrade pip && \
  locale-gen en_US.UTF-8  && \
  rm -rf /var/lib/apt/lists/*


COPY ./requirements.txt /requirements.txt
RUN pip install --upgrade -r requirements.txt && \
    python3 -m spacy download en && \
    rm -rf /root/.cache/pip

COPY . /src/
RUN cd /src && make

RUN sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
    locale-gen
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

EXPOSE 50052

WORKDIR /src
RUN chmod +x ./run.sh

ENTRYPOINT ["./run.sh"]