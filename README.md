# Screenshot service


## Build

```commandline
docker-compose build
```


## Run

Create a `data/` directory in the project root. This is where the screenshots will be saved.

```commandline
mkdir data/
```

```commandline
docker-compose up
```


## Example execution


```commandline
curl 'http://localhost:8000/screenshots/' -X POST --data '{"start_url": "https://example.com", "url_limit": 5}' -H 'Content-Type: application/json'
```
