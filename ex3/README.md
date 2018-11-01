# Start project

```sh
$ docker-compose up
```

# Open web

[Web](http://localhost:8000)

# Fetch weather to see update

```sh
# localhost:8000 should show no data yet 
# In another terminal window 
$ docker-compose exec app bash
$ pipenv run python ex3_proj/manage.py fetch_weather Saigon Paris NewYork Tokyo
# local host:8000 should show data from 3 cities after ^ command 
$ pipenv run python ex3_proj/manage.py fetch_weather Kyoto Sydney
# local host:8000 should show the new 2 cities' data after ^ command 

```
