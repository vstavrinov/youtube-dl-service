FROM alpine
ENV PATH=/srv/.local/bin:$PATH TMPDIR=/dev/shm PYTHONDONTWRITEBYTECODE=1
WORKDIR /srv
COPY youtube-dl-service.py gunicorn.conf.py yt-dlp-version ./
RUN apk update &&                                                          \
    apk add --no-cache python3 py-pip py-flask py3-gunicorn tzdata ffmpeg; \
    adduser -h /srv -D gunicorn; chown -R gunicorn:gunicorn /srv
USER gunicorn
SHELL ["/bin/ash", "-o", "pipefail", "-c"]
RUN pip install --no-cache-dir --user --break-system-packages    \
        https://github.com/vstavrinov/yt-dlp/archive/master.zip; \
        find .local -type d -name __pycache__  -print0 |         \
        xargs -0 rm -fr; rm -fr .cache;
CMD gunicorn --workers=${WORKERS:=4} --bind .0.0.0:${PORT:=8808} youtube-dl-service:app
