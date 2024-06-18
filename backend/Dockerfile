FROM python:3.10.14-alpine3.20

LABEL maintainer="thejasonlawrence1@gmail.com"
ENV PYTHONUNBUFFERED=1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./scripts /scripts
COPY ./cyto-backend-server /cyto-backend-server

WORKDIR /cyto-backend-server
EXPOSE 8000

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-build-deps \
        build-base postgresql-dev musl-dev zlib zlib-dev linux-headers && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    rm -rf /tmp && \
    apk del .tmp-build-deps && \
    adduser \ 
        --disabled-password \ 
        --no-create-home \
        django-user && \
    mkdir -p /vol/web/static && \
    chown -R django-user:django-user /vol && \
    chmod -R 755 /vol  && \
    chmod -R +x /scripts

ENV PATH="/scripts:/py/bin:$PATH"
    
USER django-user

CMD ["run.sh"] 