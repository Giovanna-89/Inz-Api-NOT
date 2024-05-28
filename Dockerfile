# Użyj wersji Pythona 3.10
FROM python:3.10-alpine3.19

# Etykieta utrzymująca
LABEL maintainer="giovanna89"

# Ustawienie zmiennej środowiskowej PYTHONBUFFERED
ENV PYTHONBUFFERED 1

# Skopiuj pliki wymagane do budowy aplikacji
COPY ./requirements.txt /tmp/requirements.txt
COPY ./app /app

# Utwórz użytkownika django-user
RUN adduser --disabled-password --no-create-home --home /app django-user

# Przełącz się do katalogu aplikacji
WORKDIR /app

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    rm -rf /tmp

ENV PATH="/py/bin:$PATH"

USER django-user

CMD ["sh", "-c", "python manage.py runserver 0.0.0.0:8000"]
