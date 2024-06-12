## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

``` 
git clone git@gitlab.com:falila/falisoftsolutions.git

cd falisoftsolutions/

python manage.py collectstatic

python manage.py runserver

```

### Docker Contenair

``` 

1. Bring up the docker stack:
   docker-compose up -d

2. Rest API is available on http://localhost:8000

3. Trigger timeseries request:
   curl -d '{"database_code":"WIKI", "dataset_code":"FB"}' -H "Content-Type: application/json" -X POST http://localhost:8000

4. Check logs:
   docker-compose logs -f

5. List cached timeseries:
   curl -X GET http://localhost:8000

6. Get timeseries:
   curl -X GET http://localhost:8000/WIKI-FB

6. Monitor tasks in flower:
   [http://localhost:5555](http://localhost:5555)
   
```

### Prerequisites

Docker contenair
Docker compose


### Installing

-- Docker docker-compose.yml compose --

```
cd falisofsolutions/

pipenv install

```

## Demo 

[AWS] https://falistore.com)

## Running the tests

```
python manage.py test

```

## Deployment
 coming soon

## Built With

* [Docker ](https://docker.com/) - Docker container
* [AWS](https://falistore.com/) - Devops

## Contributing

 Amadou KEITA

## Versioning

We use [Gitlab](https://gitlab.com/) for versioning. For the versions available, see the [tags on this repository](https://gitlab.com/falila/react_apps/). 

## Authors

* **Raphael KEITA** - *Initial work* - [](https://gitlab.com/falila/falisoftsolutions/)


## License

This project is licensed under Proprietary License - see the [LICENSE.md](LICENSE.md) file for details
