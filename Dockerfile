FROM nginx
WORKDIR /srv
ENV COLUMNS=116
ADD ydl yt-dlp-version ./
COPY nginx.conf fastcgi.conf /etc/nginx/
COPY default.conf /etc/nginx/conf.d
RUN apt-get update &&                                                 \
    apt-get install --yes --no-install-recommends                     \
        python3-pip python3-setuptools apt-utils python3-wheel        \
        ffmpeg spawn-fcgi fcgiwrap;                                   \
    pip3 install --break-system-packages                              \
        https://github.com/vstavrinov/yt-dlp/archive/master.zip;      \
    apt-get remove --yes                                              \
        python3-pip python3-setuptools apt-utils python3-wheel;       \
    rm -fr /var/cache/apt /var/lib/apt /usr/share/man /usr/share/doc; \
    usermod -d /srv www-data;                                         \
    chown -R www-data /srv /etc/nginx /var/cache/nginx
USER www-data
CMD sed -i -e "s/PORT/${PORT:=80}/"  /etc/nginx/conf.d/default.conf; \
    chmod 600 /etc/nginx/conf.d/default.conf;                        \
    spawn-fcgi -F4 -S -u www-data -p 9000 -- /usr/sbin/fcgiwrap;     \
    nginx -g "daemon off;"
