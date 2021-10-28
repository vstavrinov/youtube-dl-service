FROM nginx
WORKDIR /srv
ENV COLUMNS=116
ADD ydl .
COPY nginx.conf fastcgi.conf /etc/nginx/
COPY default.conf /etc/nginx/conf.d
RUN apt-get update &&                                                       \
    apt-get install -y --no-install-recommends                              \
        python3-pip ffmpeg fcgiwrap;                                        \
    pip3 install https://github.com/ytdl-org/youtube-dl/archive/master.zip; \
    rm -fr /var/cache/apt /var/lib/apt /usr/share/man /usr/share/doc;       \
    usermod -d /srv www-data;                                               \
    chown -R www-data /srv /etc/nginx /var/cache/nginx;                     \
    ln -sf /usr/share/zoneinfo/Europe/Moscow /etc/localtime
USER www-data
CMD sed -i -e "s/PORT/$PORT/"  /etc/nginx/conf.d/default.conf;                   \
    chmod 600 /etc/nginx/conf.d/default.conf;                                    \
    spawn-fcgi -F4 -S -u www-data -s /srv/fcgiwrap.socket -- /usr/sbin/fcgiwrap; \
    nginx -g "daemon off;"
