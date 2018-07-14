# ss-pygre
Simple &amp; stupid "rest" api select caller for PostgreSQL. Made for integration testing via Postman.

Installation:
```
pip install -r requirements.txt
```

Run Flask api "server":

```
python ss_pygre.py 
```

That's it, you can make select requests to your PostgreSQL database. For example:
```
curl -ksi -d '{"sql": "SELECT * from plan LIMIT 1", "dbname": "some_db_name", "host": "0.0.0.0", "port": 5432, "username": "postgres", "password": "password"}' -H 'Content-type: application/json' localhost:5000/anything/
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 283
Server: Werkzeug/0.14.1 Python/3.6.3
Date: Sat, 14 Jul 2018 04:00:03 GMT

[
  { 
    "created": "Wed, 17 Feb 2016 06:44:09 GMT", 
    "id": 1, 
    "plan": "FREE", 
    "price": null, 
  }
]
```

or you can do it like that using database connection string:
```
curl -ksi -d '{"sql": "SELECT * from plan LIMIT 1", "dcs": "dbname=some_db_name host=0.0.0.0 port=5432 user=postgres password=password"}' -H 'Content-type: application/json' localhost:5000/anything/
```

it also can be used to supply additional params.

You can also use default params using `config.py`, just uncomment and add your values:
```
# DBNAME = 'some_db_name'
# USERNAME = 'postgres'
# PASSWORD = 'password'
# HOST = '0.0.0.0'
# PORT = 5432
# DCS = None
```
