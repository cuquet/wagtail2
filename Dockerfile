FROM python:3.7-alpine

ADD req_docker.txt /requirements/
ADD requirements.txt /requirements/
RUN set -ex \
        && apk add --no-cache --virtual .build-deps \
                gcc \
                g++ \
                make \
                libc-dev \
                musl-dev \
                linux-headers \
                pcre-dev \
                postgresql-dev \
                libjpeg-turbo-dev \
                zlib-dev \
                git \
#       && pyvenv /venv \
        && python3 -m venv /venv \
        && /venv/bin/pip install -U pip \
        && LIBRARY_PATH=/lib:/usr/lib /bin/sh -c "/venv/bin/pip install -r /requirements/req_docker.txt" \
        && runDeps="$( \
                scanelf --needed --nobanner --recursive /venv \
                        | awk '{ gsub(/,/, "\nso:", $2); print "so:" $2 }' \
                        | sort -u \
                        | xargs -r apk info --installed \
                        | sort -u \
        )" \
        && apk add --virtual .python-rundeps $runDeps \
        && apk del .build-deps \
        && apk add libjpeg-turbo pcre
# RUN apk add --no-cache mysql-client
RUN apk add --no-cache postgresql-client
RUN mkdir -p /var/www/webapp/media
WORKDIR /var/www/
ADD . /var/www/
EXPOSE 8000

# Add custom environment variables needed by Django or your settings file here:
ENV DJANGO_SETTINGS_MODULE=webapp.settings.production DJANGO_DEBUG=off

# uWSGI configuration (customize as needed):
ENV UWSGI_VIRTUALENV=/venv UWSGI_WSGI_FILE=webapp/wsgi_production.py UWSGI_HTTP=:8000 UWSGI_MASTER=1 UWSGI_WORKERS=2 UWSGI_THREADS=8 UWSGI_UID=1000 UWSGI_GID=2000

# Call collectstatic with dummy environment variables:
# RUN DATABASE_URL=mysql://none REDIS_URL=none /venv/bin/python manage.py collectstatic --noinput
RUN DATABASE_URL=postgres://none REDIS_URL=none /venv/bin/python manage.py collectstatic --noinput --clear --ignore=*.scss -v 3

# make sure static files are writable by uWSGI process
RUN chown -R 1000:2000 /var/www/webapp/media

# start uWSGI, using a wrapper script to allow us to easily add more commands to container startup:
ENTRYPOINT ["/var/www/docker-entrypoint.sh"]
CMD ["/venv/bin/uwsgi", "--http-auto-chunked", "--http-keepalive", "--static-map", "/media/=/var/www/webapp/media/"]
