cmd=$1
tag=$(git describe --always)

usage() {
    echo "Usage: deploy.sh <command>"
    echo "Available commands:"
    echo "build             Build Docker image for the app and monitoring service"
    echo "up                Run app and monitoring service container"
    # echo "push              Push Docker image to registry"
    # echo "build_and_push    Build and push Docker image to registry"
}

if [[ -z "$cmd" ]]; 
then
    echo "Missing command"
    usage
    exit 1
fi

APP_IMAGE_NAME="emotion_analysis/app"
MONITORING_SERVICE_IMAGE_NAME="emotion_analysis/monitoring-service"

# Chuyển đến root folder của project
cd "$(dirname "$0")/../" || exit 1

build() {
    # docker build -f emotion_analysis/Dockerfile.main -t $APP_IMAGE_NAME:$tag .
    # docker tag $APP_IMAGE_NAME:$tag $APP_IMAGE_NAME:latest

    docker build -f emotion_analysis/Dockerfile.monitor -t $MONITORING_SERVICE_IMAGE_NAME:$tag .
    docker tag $MONITORING_SERVICE_IMAGE_NAME:$tag $MONITORING_SERVICE_IMAGE_NAME:latest
}

up() {
    # docker run --network shared-network -p 8765:8765 --name emotion-analysis-service $APP_IMAGE_NAME
    docker run --network shared-network -p 8767:8767 --name monitoring-service $MONITORING_SERVICE_IMAGE_NAME
}

# push() {
#     docker push $APP_IMAGE_NAME:$tag
#     docker push $IMAGE_NAME:latest
# }

case $cmd in
    build)
        build
        ;;
    up)
        up
        ;;
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