FROM python:3.6

RUN pip install django cx_Oracle

COPY . /app

WORKDIR /app

RUN pip install django-cors-headers

RUN python manage.py migrate

CMD ["python", "manage.py", "runserver"]