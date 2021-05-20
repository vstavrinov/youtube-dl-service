# youtube-dl-service

This video streaming service based on [youtube-dl](https://github.com/ytdl-org/youtube-dl) project. It extracts stream from web page and feeds it directly to Your video player allowing to avoid using browser. You can run it either on local computer or on the cloud turning it into global service.

## Build:

```
git clone https://github.com/vstavrinov/youtube-dl-service.git
cd youtube-dl-service
docker build -t youtube-dl-service .
```

## Usage:

```
docker run -d -e PORT=<service-port> -p <container-port>:<service-port> <youtube-dl-image>
```

- service-port is port of service inside container.
- container-port is where you send your request for stream
- youtube-dl-image is either docker image You build on your own or those pulled from the repository.

For example:

```
docker run -d -e PORT=7000 -p 8000:7000 youtube-dl-service
```
Or you can omit build phase and pull and run it from the repository:

```
docker run -d -e PORT=7000 -p 8000:7000 vstavrinov/youtube-dl-service
```

Finally you can watch tv:

```
vlc --playlist-autostart http://localhost:8000?youtube.com/BloombergTV/live
```

Here 'youtube.com/BloombergTV/live' is URL of web page where You watch this stream with browser. Check for all available formats for this stream:

```
curl 'http://localhost:8000?youtube.com/BloombergTV/live&list-formats'
```

To get the list of supported sites for streaming:

```
curl 'http://localhost:8000?extractor-descriptions'
```

See more available options:

```
curl http://localhost:8000?help
```

Use only long options with \"--\" stripped and concatenated with an ampersand. You can put these options into query string of the form:

```
key1=value1&key2=value2&key3&key4 etc.
```

For example using on of the format listed above:

```
vlc --playlist-autostart 'http://localhost:8000?youtube.com/BloombergTV/live&format=300'
```

If You provide a URL it must be the first option. Needless to say You can use any player instead vlc and browser your prefer instead curl.
