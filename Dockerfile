FROM alpine:3.10.3

# This hack is widely applied to avoid python printing issues in docker containers.
# See: https://github.com/Docker-Hub-frolvlad/docker-alpine-python3/pull/13
# ENV PYTHONUNBUFFERED=1

RUN apk add --update python3 git gcc python3-dev musl-dev && \
    rm  -rf /tmp/* /var/cache/apk/* && \
    if [ ! -e /usr/bin/python ]; then ln -sf python3 /usr/bin/python ; fi && \
    \
    echo "**** install pip ****" && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --no-cache --upgrade pip setuptools wheel && \
    if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi

RUN git clone https://github.com/Tuxae/Twitter-DiscordBot && \
    mv Twitter-DiscordBot/* . && \
    rm -r Twitter-DiscordBot && \
    pip3 install discord requests asyncio beautifulsoup4

COPY my_constants.py .

CMD ["python3", "twitter.py"]

