<p align="center"><img src="https://img.shields.io/badge/Version-1.0.0-brightgreen"></p>
<p align="center">
  <a href="https://github.com/mdminhaz2003">
    <img src="https://img.shields.io/github/followers/mdminhaz2003?label=Follow&style=social">
  </a>
</p>
<p align="center">
</p>

---

# GTFS Arrivals API Docs

## Install
```commandline
pip install -r requirements.txt
```
## Run the supervisor
```commandline
mkdir -p logs && supervisord -c supervisord.conf
```
## Check the status
```commandline
supervisorctl status
```
## Stop process
```commandline
supervisorctl stop <process_name>
```
## Update process
```commandline
supervisorctl reread
```
```commandline
supervisorctl update
```
## Kill the process
```commandline
kill <pid>
```
## Run the api
```commandline
flask run --host=0.0.0.0
```
# REST API

The GTFS Arrivals app's REST API is described below.

## Get list of Things

### Request

`GET /`
```commandline
curl -i -H 'Accept: application/json' http://localhost:5000/
```
### Response
```json
{
  "app": "GTFS Stops",
  "version": "1.0.0"
}
```
`GET /stops/<stop_id>?skip=0&limit=100&date=2023-03-29&time=25:26:24&tz=3.9`
#### params
`skip=10 (Optional)` `Default 0`<br>
`limit=100 (Optional)` `Default 10`<br>
`date=2023-03-29 (Optional)` `Default Current UTC Date`<br>
`time=25:26:24 (Optional)` `Default Current UTC Time`<br>
`tz=3.9 (Optional)` `Default UTC timezone`
```commandline
curl -i -H 'Accept: application/json' http://localhost:5000/arrival/9400ZZLUSJP2
```

`GET /update-data/<passcode>?url=https://example.com/gtfs-data.zip`
#### params
`url (optional)`<br>
`default url -> https://data.bus-data.dft.gov.uk/timetable/download/gtfs-file/all/`
```commandline
curl -i -H 'Accept: application/json' http://localhost:5000/update-data/passcode
```
`GET /status/<task-id>`
```commandline
curl -i -H 'Accept: application/json' http://localhost:5000/status/task-id
```

`GET /clear-cache/<passcode>`
```commandline
curl -i -H 'Accept: application/json' http://localhost:500/clear-cache/:passcode
```

### Check databases
```commandline
\dt
```
### Example Response


| **`Schema`** | **`Name`**  | **`Type`** | **`Owner`** |
|--------------|-------------|------------|-------------|
| public       | calendar    | table      | admin       |
| public       | routes      | table      | admin       |
| public       | stop_times  | table      | admin       |
| public       | stops       | table      | admin       |
| public       | trips       | table      | admin       |


### Get all available Stops
```sqlite-psql
SELECT
    stops.stop_id,
    stops.stop_name,
    trips.trip_headsign as destination,
    routes.route_short_name as route_name,
    stop_times.arrival_time + current_date as arrival_datetime,
    stop_times.departure_time + current_date as departure_datetime
FROM stops
JOIN stop_times ON stops.stop_id = stop_times.stop_id
JOIN trips ON stop_times.trip_id = trips.trip_id
JOIN routes ON trips.route_id = routes.route_id
JOIN calendar ON trips.service_id = calendar.service_id
WHERE
    CASE
        WHEN date_part('dow', current_date) = 0 THEN calendar.sunday
        WHEN date_part('dow', current_date) = 1 THEN calendar.monday
        WHEN date_part('dow', current_date) = 2 THEN calendar.tuesday
        WHEN date_part('dow', current_date) = 3 THEN calendar.wednesday
        WHEN date_part('dow', current_date) = 4 THEN calendar.thursday
        WHEN date_part('dow', current_date) = 5 THEN calendar.friday
        WHEN date_part('dow', current_date) = 6 THEN calendar.saturday
    END = 't'
    AND current_date >= start_date
    AND current_date <= end_date
    AND current_timestamp <= stop_times.arrival_time + current_date
    AND current_date = date(stop_times.arrival_time + current_date)
ORDER By arrival_datetime
LIMIT 100 OFFSET 0;
```

### Get Stops by stop_id
```sqlite-psql
SELECT
    stops.stop_id,
    stops.stop_name,
    trips.trip_headsign as destination,
    routes.route_short_name as route_name,
    stop_times.arrival_time + current_date as arrival_datetime,
    stop_times.departure_time + current_date as departure_datetime
FROM stops
JOIN stop_times ON stops.stop_id = stop_times.stop_id
JOIN trips ON stop_times.trip_id = trips.trip_id
JOIN routes ON trips.route_id = routes.route_id
JOIN calendar ON trips.service_id = calendar.service_id
WHERE
    stops.stop_id = <stop_id>
    AND CASE
        WHEN date_part('dow', current_date) = 0 THEN calendar.sunday
        WHEN date_part('dow', current_date) = 1 THEN calendar.monday
        WHEN date_part('dow', current_date) = 2 THEN calendar.tuesday
        WHEN date_part('dow', current_date) = 3 THEN calendar.wednesday
        WHEN date_part('dow', current_date) = 4 THEN calendar.thursday
        WHEN date_part('dow', current_date) = 5 THEN calendar.friday
        WHEN date_part('dow', current_date) = 6 THEN calendar.saturday
    END = 't'
    AND current_date >= calendar.start_date
    AND current_date <= calendar.end_date
    AND current_timestamp <= stop_times.arrival_time + current_date
    AND current_date = date(stop_times.arrival_time + current_date)
ORDER BY arrival_datetime
LIMIT 100 OFFSET 0;
```

### Response Table should be
| **`stop_id`** | **`stop_name`**               | **`destination`** | **`route_name`** | **`arrival_datetime`** | **`departure_datetime`** |
|---------------|-------------------------------|-------------------|------------------|------------------------|--------------------------|
| 0500CCITY202  | Hospital Bus Station (Bay C)  | Little Wratting   | 13               | 2023-03-24 00:00:00    | 2023-03-24 00:00:00      |
| 0500CCITY497  | The Busway Shire Hall         | St Ives           | A                | 2023-03-24 00:00:00    | 2023-03-24 00:00:00      |
| 390061097     | Ordnance House                | Felixstowe        | 75               | 2023-03-24 00:00:00    | 2023-03-24 00:00:00      |
| 0500CCITY057  | Perse School                  | Fulbourn          | 1                | 2023-03-24 00:00:00    | 2023-03-24 00:00:00      |
| 0500HSTNS064  | Market Square (Stop D)        | St Neots          | 905              | 2023-03-24 00:00:00    | 2023-03-24 00:00:00      |



---
[Be Connected](https://www.github.com/mdminhaz2003/)
========

<p align="center">
    <a href="https://www.buymeacoffee.com/mdminhaz2003"><img src="https://img.shields.io/badge/-Buy me a coffee-000000?style=for-the-badge&logo=buymeacoffee&logoColor=yellow"/></a>
    <a href="https://www.youtube.com/easycoding2021/"><img src="https://img.shields.io/badge/-Easy Coding-FF0000?style=for-the-badge&logo=YouTube&logoColor=white"/></a>
    <a href="https://www.facebook.com/mdminhaz2003/"><img src="https://img.shields.io/badge/-Md. Minhaz-3423A6?style=for-the-badge&logo=Facebook&logoColor=white"/></a>
    <a href="https://www.linkedin.com/in/mdminhaz2003/"><img src="https://img.shields.io/badge/-Md. Minhaz-0077B5?style=for-the-badge&logo=Linkedin&logoColor=white"/></a>
    <a href="mailto:mdm047767@gmail.com"><img src="https://img.shields.io/badge/-Mail-D14836?style=for-the-badge&logo=Gmail&logoColor=white"/></a>
    <a href="https://instagram.com/mdminhaz2003/"><img src="https://img.shields.io/badge/-Md. Minhaz-E4405F?style=for-the-badge&logo=Instagram&logoColor=white"/></a>
    <a href="https://twitter.com/easycoding2021/"><img src="https://img.shields.io/badge/-Easy Coding-1DA1F2?style=for-the-badge&logo=twitter&logoColor=white"/></a>
</p>