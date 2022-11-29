# Sentiment Classification Project for Text Analytics
## Project details
#### Title: 
Sentiment Classification Project for Text Analytics

#### Team members: 
- Pascal Hansen (pascal.hansen@stud.uni-heidelberg.de)
- Simon Pavicic (simon.pavicic@stud.uni-heidelberg.de)
- Maximilian Ludwig (maximilian.ludwig02@stud.uni-heidelberg.de)

#### Existing code fragments
In this project we will use the githup project https://github.com/workmanjack/lyric-mood-classification as starting point. We will utilize the devloped CNN for mood classification based on lyrics in this project an apply it to our dataset.

#### Utilized librarires
The project is runnable by simply using the command ``` docker-compose up ```, which builds and starts all necessary services. Only docker (preferrably in Linux or WSL2) is a prerequisite. Please note that it might take up to ~5 minutes to start the application properly, based on your System.

#### Contributions
See commit history. 


## Project state
#### Planning state


#### Future planning 


#### High-level architecture description


#### Data analysis 
For a detailed description of the data analysis performed please see ta_lyrics_sentiment_classification/data_exploration/readme.md as well as the jupyter notebooks found under ta_lyrics_sentiment_classification/data_exploration/.

#### Experiments 



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

### Update the images
When you update the dockerfiles or let's say the npm dependencies (basically anything that needs to be build) you might want to run ``` docker-compose build ``` to create a new image version. Otherwise the container might not have the correct dependencies injected


## Coding guidelines
Function and class descriptions will follow the Sphinx guidline as shown here: https://sphinx-rtd-tutorial.readthedocs.io/en/latest/docstrings.html.


## Troubleshooting:
### The application takes so long to start
If you are using windows, try to clone the repository into your wsl file system and run it from there. Especially the frontend is runinng extremly slow otherwise
