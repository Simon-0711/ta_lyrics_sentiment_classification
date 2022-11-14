# Sentiment Classification Project for Text Analytics
## Project details
#### Title: Sentiment Classification Project for Text Analytics
#### Team members: 
Pascal Hansen (pascal.hansen@stud.uni-heidelberg.de)
Simon Pavicic (simon.pavicic@stud.uni-heidelberg.de)
Maximilian Ludwig (maximilian.ludwig02@stud.uni-heidelberg.de)

#### Existing code fragments
In this project we will use the githup project https://github.com/workmanjack/lyric-mood-classification as starting point. We will utilize the devloped CNN for mood classification based on lyrics in this project an apply it to our dataset.

#### Utilized librarires
The project is runnable by simply using the command ``` docker-compose up ```, which builds and starts all necessary services. Only docker (preferrably in Linux or WSL2) is a prerequisite.

#### Contributions




## Start guide

Clone the repository and run from the root of it:
``` docker-compose up ```
This will start up the docker containers specified in the docker-compose file.
After that you should be able to see them with ``` docker ps ```. 
If you want to connect to them use ``` docker exec -it <container_name or ID> /bin/sh ```

You can then start ot stop these services at anytime by typing
```
docker-compse start 
docker-compose stop
```

The startup may take a while. When the appearing log messages in the terminal are stalling, the app should be ready to use.
Kibana is accessed by http://localhost:5601
Elasticsearch is accessed by http://localhost:9200
Fasatpi is accessed by http://localhost:8000
Fasatpi is accessed by http://localhost:3000

### Start up only certain services
To start only certain services like fastapi or elasticsearch or kibana, you can use the following command:
```
docker-compose start <servicename>
```
Please note that this might only work if you have run previously 
```
docker-compose up
```
and stopped the container services.