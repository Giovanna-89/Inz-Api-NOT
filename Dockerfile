# Użyj wersji Pythona 3.10
FROM python:3.10-alpine3.19

# Etykieta utrzymująca
LABEL maintainer="giovanna89"

# Ustawienie zmiennej środowiskowej PYTHONBUFFERED
ENV PYTHONBUFFERED 1

# Skopiuj pliki wymagane do budowy aplikacji
COPY ./requirements.txt /tmp/requirements.txt
COPY ./app /app

# Przełącz się do katalogu aplikacji
WORKDIR /app

# Instalacja zależności systemowych i Pythonowych
RUN apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-build-deps \
        build-base postgresql-dev musl-dev && \
    python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    apk del .tmp-build-deps && \
    rm -rf /tmp

# Utwórz użytkownika django-user
RUN adduser --disabled-password --no-create-home django-user

# Ustaw PATH
ENV PATH="/py/bin:$PATH"

# Przełącz na użytkownika django-user
USER django-user

# Expose port 8000
EXPOSE 8000

# CMD do uruchomienia serwera Django
CMD ["sh", "-c", "python manage.py runserver 0.0.0.0:8000"]
