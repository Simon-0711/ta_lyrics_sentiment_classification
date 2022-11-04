# Sentiment Classification Project for Text Analytics

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