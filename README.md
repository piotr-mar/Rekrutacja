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
Before running script you have to add yours api key from openweathermap.org as API env. variable
```bash
export $API=<your api key from openweathermap>
```

Inside docker in repo dir type:
```bash
python3 manage.py makemigrations

python3 manage.py migrate

python3 manage.py runserver
```
In web browser go to address: http://127.0.0.1:8000/

If you want to create superuser run command:
```bash
python3 manage.py createsuperuser
```
