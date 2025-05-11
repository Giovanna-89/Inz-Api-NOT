FROM python:3.10-alpine3.19

LABEL maintainer="giovanna89"

# Avoid buffering stdout/stderr
ENV PYTHONUNBUFFERED=1

# Install dependencies and tools
RUN apk add --no-cache postgresql-client \
    && apk add --no-cache --virtual .build-deps \
        build-base postgresql-dev musl-dev

# Create working directory
WORKDIR /app

# Copy files
COPY ./requirements.txt /tmp/requirements.txt
COPY ./app /app

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install -r /tmp/requirements.txt && \
    apk del .build-deps && \
    rm -rf /tmp

# Create non-root user
RUN adduser --disabled-password --no-create-home django-user

# Set PATH
ENV PATH="/home/django-user/.local/bin:$PATH"

RUN mkdir -p /app/logs && chown -R django-user /app/logs

USER django-user

EXPOSE 8000