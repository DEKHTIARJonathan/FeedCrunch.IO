docker run -d -v "C:\Git Projects\FeedCrunch.IO":"/app" --name feedcrunch_dev continuumio/miniconda3 tail -f /dev/null
docker exec -it feedcrunch_dev bash

##############

docker run -d --name feedcrunch feedcrunch tail -f /dev/null
docker exec -it feedcrunch_1 bash