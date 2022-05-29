```
Clone
$ git clone <this_project>
$ cd <this_project>

Create sqlite3 file in advance to mount into container
Ensure that, *.sqlite3 file name is matching in .env `sqlite_path` variable  
$ touch bitcoindb.sqlite3

To start the server
$ docker-compose up --build -d

To test the api, use curl or Or point the url in your favourite browser.
$ curl http://localhost:8000/api/prices/btc?date=29-03-2022

To stop the server
$ docker-compose down

```

##### Configured persistent volume(type=bind-host) for database

so we can safely use `docker-compose down`

NOTE: As an alternate, we can use `Docker plugin` in editor=Pycharm Community Edition

---




