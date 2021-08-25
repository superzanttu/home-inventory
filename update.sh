echo --- Updating Hiapp app image
./build.sh && ./run.sh
echo --- Remove dangling images
docker images --no-trunc -aqf "dangling=true" | xargs docker rmi
echo --- Docker images
docker images
echo --- Docker containers
docker ps -a
