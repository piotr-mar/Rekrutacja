# Zadanie rekrutacyjne

## Docker
### Docker Install
You have to have docker and docker compose-plugin. <br>
Installation: check here [link](https://docs.docker.com/engine/install/ubuntu/)

### Building docker container
For building docker run command:
```bash
    docker compose build weather-web-dev
```

### Run docker container
```bash
  docker compose run weather-web-dev
```

You can also use run command to build and run docker container.

## WeatherApp
Inside docker in repo dir type:
```bash
python3 manage.py 
```