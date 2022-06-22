docker_image_tag="registry.deti:5000/egs4/frontend:latest"

cd ../client
npm run build

cd ..

docker build -t $docker_image_tag -f deploy/Dockerfile .
docker image push $docker_image_tag