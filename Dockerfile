FROM python:3.9-buster
ENV PYTHONUNBUFFERED=1
WORKDIR /code
RUN apt-get update \
    && apt-get install -y --no-install-recommends gettext \
    postgresql-client
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/
EXPOSE 8000
CMD ["/bin/bash", "-c", "printenv | grep -v \"no_proxy\" >> /etc/environment; python manage.py migrate; python manage.py runserver 0.0.0.0:8000"]