# youtube-dl-service

This video streaming service based on [yt-dlp](https://github.com/yt-dlp/yt-dlp) project. It extracts stream from web page and feeds it directly to Your video player allowing to avoid using browser. You can run it either on local computer or on the cloud turning it into global service.

## Simplest Quik Start

```
docker run -p 8808:8808 vstavrinov/youtube-dl-service
```

## Build:

```
git clone https://github.com/vstavrinov/youtube-dl-service.git
cd youtube-dl-service
docker build -t youtube-dl-service .
```

## Usage:

```
docker run -d -e WORKERS=<workers> -e PORT=<service-port> -p <container-port>:<service-port> <youtube-dl-image>
```

- service-port is port of service inside container (default 8808).
- container-port is where you send your request for stream
- youtube-dl-image is either docker image You build on your own or those pulled from the repository.
- workers-number is max clients served simultaneously (default 4).

For example:

```
docker run -d -e PORT=8808 -p 8808:8808 youtube-dl-service
```
Or you can omit build phase and pull and run it from the repository:

```
docker run -d -e PORT=8808 -p 8808:8808 vstavrinov/youtube-dl-service
```

Finally you can watch tv:

```
vlc --playlist-autostart http://localhost:8808/youtube.com/BloombergTV/live
```

Here 'youtube.com/BloombergTV/live' is URL of web page where You watch this stream with browser. Check for all available formats for this stream:

```
curl 'http://localhost:8808/youtube.com/BloombergTV/live?--list-formats'
```

To get the list of supported sites for streaming:

```
curl 'http://localhost:8808?--extractor-descriptions'
```

See more available options:

```
curl http://localhost:8808?--help
```

Use only long options concatenated with an ampersand. You can put these options into query string of the form:

```
key1=value1&key2=value2&key3&key4 etc.
```
Be aware, if the stream URL has no query string, You must prepend the options with a question mark. And any options must follow stream URL.
For example using one of the format listed above:

```
vlc --playlist-autostart 'http://localhost:8808/youtube.com/BloombergTV/live?--format=230'
```

If You provide a URL it must be the first option. Needless to say You can use any player instead vlc and browser your prefer instead curl.


## Update

The docker image automatically updated with [yt-dlp](https://github.com/yt-dlp/yt-dlp) every update. So to get image for your service up to date do the following in that order: 

1. Stop your docker container. 
2. Remove Your docker container. 
3. Remove your docker image. 
4. Run your docker container.

