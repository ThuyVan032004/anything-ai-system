service=$1
cmd=$2

AIRFLOW="airflow"
ELK="elk"
FEAST="feast"
GRAFANA="grafana"
PROMETHEUS="prometheus"
JENKINS="jenkins"
MLFLOW="mlflow"
SLEEP_TIME=2

usage() {
    echo "Command: run.sh <service> <command> [options]"
    echo "Available services:"
    echo "all:              All services"
    echo "airflow:          Airflow service"
    echo "elk:              ELK service"
    echo "feast:            Feast service"
    echo "grafana:          Grafana service"
    echo "prometheus:       Prometheus service"
    echo "jenkins:          Jenkins service"
    echo "mlflow:           MLflow service"
    echo "Available commands:"
    echo "up:               Start the service"
    echo "down:             Stop the service"
    echo "restart:          Restart the service"
    echo "Available options:"
    echo "--build:          Rebuild images before starting containers"
}

up() {
    local service_name=$1
    shift
    docker_compose_file="$service_name/$service_name-docker-compose.yml"
    docker-compose -f $docker_compose_file up -d "$@"
}

airflow_up() {
    up "$AIRFLOW" "$@"
}

elk_up() {
    up "$ELK" "$@"
}

feast_up() {
    up "$FEAST" "$@"
}

grafana_up() {
    up "$GRAFANA" "$@"
}

prometheus_up() {
    up "$PROMETHEUS" "$@"
}

jenkins_up() {
    up "$JENKINS" "$@"
}

mlflow_up() {
    up "$MLFLOW" "$@"
}

down() {
    local service_name=$1
    shift
    docker_compose_file="$service_name/$service_name-docker-compose.yml"
    docker-compose -f $docker_compose_file down -d "$@"
}

airflow_down() {
    down "$AIRFLOW" "$@"
}

elk_down() {
    down "$ELK" "$@"
}

feast_down() {
    down "$FEAST" "$@"
}

grafana_down() {
    down "$GRAFANA" "$@"
}

prometheus_down() {
    down "$PROMETHEUS" "$@"
}

jenkins_down() {
    down "$JENKINS" "$@"
}

mlflow_down() {
    down "$MLFLOW" "$@"
}

airflow_restart() {
    down "$AIRFLOW" "$@"
    sleep "$SLEEP_TIME"
    up "$AIRFLOW" "$@"
}

elk_restart() {
    down "$ELK" "$@"
    sleep "$SLEEP_TIME"
    up "$ELK" "$@"
    
}

feast_restart() {
    down "$FEAST" "$@"
    sleep "$SLEEP_TIME"
    up "$FEAST" "$@"
}

grafana_restart() {
    down "$GRAFANA" "$@"
    sleep "$SLEEP_TIME"
    up "$GRAFANA" "$@"
}

prometheus_restart() {
    down "$PROMETHEUS" "$@"
    sleep "$SLEEP_TIME"
    up "$PROMETHEUS" "$@"
}

jenkins_restart() {
    down "$JENKINS" "$@"
    sleep "$SLEEP_TIME"
    up "$JENKINS" "$@"
}

mlflow_restart() {
    down "$MLFLOW" "$@"
    sleep "$SLEEP_TIME"
    up "$MLFLOW" "$@"
}

if [[ -z "$service" ]];
then
    echo "Missing service"
    usage
    exit 1
fi

if [[ -z "$cmd" ]];
then
    echo "Missing command"
    usage
    exit 1
fi

# shift the first two arguments to the left
shift 2

case $cmd in
    up)
        case $service in
            all)
                airflow_up
                elk_up
                feast_up
                grafana_up
                prometheus_up
                jenkins_up
                mlflow_up
                ;;
            airflow)
                airflow_up
                ;;
            elk)
                elk_up
                ;;
            feast)
                feast_up
                ;;
            grafana)
                grafana_up
                ;;
            prometheus)
                prometheus_up
                ;;
            jenkins)
                jenkins_up
                ;;
            mlflow)
                mlflow_up
                ;;
            *)
                echo "Unknown service: $service"
                usage
                exit 1
                ;;
        esac
    
        ;;
    down)
        case $service in
            all)
                airflow_down
                elk_down
                feast_down
                grafana_down
                prometheus_down
                jenkins_down
                mlflow_down
                ;;
            airflow)
                airflow_down
                ;;
            elk)
                elk_down
                ;;
            feast)
                feast_down
                ;;
            grafana)
                grafana_down
                ;;
            prometheus)
                prometheus_down
                ;;
            jenkins)
                jenkins_down
                ;;
            mlflow)
                mlflow_down
                ;;
            *)
                echo "Unknown service: $service"
                usage
                exit 1
                ;;
        esac

        ;;
    restart)
        case $service in
            all)
                airflow_restart
                elk_restart
                feast_restart
                grafana_restart
                prometheus_restart
                jenkins_restart
                mlflow_restart
                ;;
            airflow)
                airflow_restart
                ;;
            elk)
                elk_restart
                ;;
            feast)
                feast_restart
                ;;
            grafana)
                grafana_restart
                ;;
            prometheus)
                prometheus_restart
                ;;
            jenkins)
                jenkins_restart
                ;;
            mlflow)
                mlflow_restart
                ;;
            *)
                echo "Unknown service: $service"
                usage
                exit 1
                ;;
        esac

        ;;
    
    *)
        echo "Unknown command: $cmd"
        usage
        exit 1
        ;;
esac


