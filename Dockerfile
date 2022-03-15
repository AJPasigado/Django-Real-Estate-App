FROM library/postgres
COPY ./docker-services/postgresql/init-user-db.sh /docker-entrypoint-initdb.d/

FROM python:2.7.14
ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code

ADD ./requirements/local.txt /code/requirements.txt
ADD ./requirements/base.txt /code/
RUN pip install -r requirements.txt

EXPOSE 80 8000 5432

ADD . /code
RUN python manage.py collectstatic --clear --noinput
# RUN python manage.py migrate
