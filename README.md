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