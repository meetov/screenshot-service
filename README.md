# Screenshot service


## Build

```commandline
docker-compose build
```


## Run

```commandline
docker-compose up
```


## Example execution


```commandline
curl 'http://localhost:8000/screenshots/' -X POST --data '{"start_url": "https://example.com", "url_limit": 5}' -H 'Content-Type: application/json'
```