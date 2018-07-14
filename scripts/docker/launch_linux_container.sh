docker run -d -v "C:\Git Projects\FeedCrunch.IO":"/app" --name feedcrunch_1 continuumio/miniconda3 tail -f /dev/null
docker exec -it feedcrunch_1 bash