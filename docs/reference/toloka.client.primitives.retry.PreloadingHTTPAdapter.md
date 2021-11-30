# PreloadingHTTPAdapter
`toloka.client.primitives.retry.PreloadingHTTPAdapter`

HTTPAdapter subclass that forces preload_content=True during requests


As for current version (2.26.0) requests supports body preloading with stream=False, but this behaviour is
implemented by calling response.content in the end of request process. Such implementation does not support
retries in case of headers being correctly received by client but body being loaded incorrectly (i.e. when server
uses chunked transfer encoding and fails during body transmission). Retries are handled on urllib3 level and
retrying failed body read can be achieved by passing preload_content=False to urllib3.response.HTTPResponse. To do
this using HTTPAdapter we need to use HTTP(S)ConnectionPool.urlopen with preload_content=True during send method and
override build_response method to populate requests Response wrapper with content.

## Methods summary

| Method | Description |
| :------| :-----------|
[build_response](toloka.client.primitives.retry.PreloadingHTTPAdapter.build_response.md)| None
[get_connection](toloka.client.primitives.retry.PreloadingHTTPAdapter.get_connection.md)| None
