FROM python:3.5

ENV EUCTR_SECRET_KEY yes
ENV EUCTR_DEBUG yes # TODO: fix to no
ENV EUCTR_OPENTRIALS_DB ""
ENV EUCTR_GOOGLE_TRACKING_ID ""
ENV EUCTR_CRAWLERA_APIKEY ""

RUN wget -q https://github.com/ebmdatalab/euctr-tracker-code/archive/master.zip -O /tmp/code.zip \
  && unzip /tmp/code.zip -d / \
  && mv /euctr-tracker-code-master /euctr-tracker-code \
  && rm /tmp/code.zip

RUN pip install --no-cache-dir -r /euctr-tracker-code/requirements.txt

RUN wget -q https://github.com/ebmdatalab/euctr-tracker-data/archive/master.zip -O /tmp/data.zip \
  && unzip /tmp/data.zip -d / \
  && mv /euctr-tracker-data-master /euctr-tracker-data \
  && rm /tmp/data.zip

WORKDIR /euctr-tracker-code/euctr

#RUN ./manage.py collectstatic --noinput
#RUN apt-get update && apt-get install -y nginx && apt-get clean && rm -rf /var/lib/apt/lists/*

EXPOSE 8000
ENTRYPOINT ["./manage.py"]
CMD ["runserver", "0.0.0.0:8000"]

