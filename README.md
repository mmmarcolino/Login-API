# Login-Api

## Requirements
   - python >= 3.9 
   - venv
   - MySql database (running on localhost -cfr. configuration files 
   i.e. `login_api/config`)
   - executing the queries in login_api.sql (to have basic data added to Database)
   - memcached
   - activate memcached (run `memcached` in command line)

## Run
To run the app the environment variable (cfr. `login_api/config/.env`) 
must be set to `dev`.  
From project home activate `venv` then install requirements (cfr. `requirements.txt`) 
and finally run the app:  
   - `source venv/bin/activate`
   - `python -m pip install -r requirements`
   - `python -m login_api.app`

## Test
To execute test run from project home:
`pytest --cov=login_api test/`


## Docker
To run docker the environment variable (cfr. `login_api/config/.env`) 
must be set to `docker`.  
To run the docker-app run from project home:  
`sudo docker-compose up --build`  
To test the app connect to docker database run:  
`docker exec -it  db_login mysql -uroot -ppassword`  
and then execute the queries provided in `docker.sql`.
