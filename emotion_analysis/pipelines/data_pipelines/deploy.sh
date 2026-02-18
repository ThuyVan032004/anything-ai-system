cmd=$1
tag=$(git describe --always)

usage() {
    echo "Usage: deploy.sh <command>"
    echo "Available commands:"
    echo "build             Build Docker image"
    # echo "push              Push Docker image to registry"
    # echo "build_and_push    Build and push Docker image to registry"
}

if [[ -z "$cmd" ]]; 
then
    echo "Missing command"
    usage
    exit 1
fi

IMAGE_NAME="emotion_analysis/data_pipelines"

# Chuyển đến root folder của project
cd "$(dirname "$0")/../../../" || exit 1

build() {
    docker build -f emotion_analysis/pipelines/data_pipelines/Dockerfile -t $IMAGE_NAME:$tag .
    docker tag $IMAGE_NAME:$tag $IMAGE_NAME:latest
}

# push() {
#     docker push $IMAGE_NAME:$tag
#     docker push $IMAGE_NAME:latest
# }

case $cmd in
    build)
        build
        ;;
    # push)
    #     push
    #     ;;
    # build_and_push)
    #     build
    #     push
    #     ;;
    *)
        echo "Invalid command: $cmd"
        usage
        exit 1
        ;;
esac