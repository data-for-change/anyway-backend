# anyway-backend


------

## Getting the code
1. [Fork](https://github.com/hasadna/anyway-backend/fork) this repository on GitHub
1. `git clone https://github.com/*you*/anyway-backend`
1. Add the main repository as your upstream remote: `git remote add upstream https://github.com/hasadna/anyway-backend`


# ANYWAY’s docker environment
-----------------------

Read more about DOCKER at [Offical docs](https://docs.docker.com/) or at [Github project](https://github.com/docker/docker)

There are 2 Dockerfiles in this project :
1) The PostgreSQL DB docker at the "db_docker" folder
2) The actual backend application docker is the Dockerfile


#### ReBuild & ReRun
If you change the docker files and want to re-run the docker-compose you need to:

`docker-compose build` and then: `docker-compose up`

For the first time, and for any postgres schema changes (we are using alembic), run, when containers are up:
`docker exec -it anyway-backend_anyway_1 alembic upgrade head`

docker-postgis - Dockerfile, initdb-postgis.sh and update-postgis.sh where inspired from here:
`https://github.com/appropriate/docker-postgis/tree/f6d28e4a1871b1f72e1c893ff103f10b6d7cb6e1/10-2.4`


#### Load CBS DATA
1. Copy the following [cbs data directory](https://drive.google.com/drive/folders/1JVBNP3oTn12zxWExPKeCf_vetNHVCcoo?usp=sharing) into data (hence data will be in the path: data/cbs/...)
2. make sure the docker is up - run `docker-compose up -d`
3. `docker exec -it anyway-backend_anyway_1 bash -c "python main.py process road-segments"`
4. `docker exec -it anyway-backend_anyway_1 bash -c "python main.py process cbs"`
5. Grab a cup of coffee, this will take ~1 hour

#### Altering the database using alembic
1. Adding a schema: create a schema revision, [for example](https://github.com/hasadna/anyway-backend/blob/dev/alembic/versions/ab9834c903dd_add_waze_schema.py)
2. Adding or modifying a table:
When creating a patch that alters the database schema, you should use generate the appropriate
[Alembic](http://alembic.zzzcomputing.com/en/latest/index.html) revision by running:

`docker exec -it anyway-backend_anyway_1 bash -c "alembic revision --autogenerate -m 'Description of the change'"`

```
