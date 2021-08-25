echo --- Stopping and removing old container version
docker rm -f Hiapp
echo --- Starting new version of container
docker run -p 80:80 -d -v /Users/santtu/Dropbox/Docker/HomeInventoryAPP:/hiapp --name Hiapp hiapp
