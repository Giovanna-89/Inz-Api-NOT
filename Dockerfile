FROM python:3.10-alpine3.19


LABEL maintainer="giovanna89"


ENV PYTHONBUFFERED 1


COPY ./requirements.txt /tmp/requirements.txt
COPY ./app /app


WORKDIR /app


RUN apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-build-deps \
        build-base postgresql-dev musl-dev && \
    python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    apk del .tmp-build-deps && \
    rm -rf /tmp


RUN adduser --disabled-password --no-create-home django-user


ENV PATH="/py/bin:$PATH"


USER django-user


EXPOSE 8000


CMD ["sh", "-c", "python manage.py runserver 0.0.0.0:8000"]



