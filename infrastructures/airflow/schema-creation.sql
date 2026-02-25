create schema if not exists airflow;
grant all privileges on schema airflow to vandtt;
alter default privileges in schema airflow grant all on tables to vandtt;
alter default privileges in schema airflow grant all on sequences to vandtt;

create schema if not exists mlflow;
grant all privileges on schema mlflow to vandtt;
alter default privileges in schema mlflow grant all on tables to vandtt;
alter default privileges in schema mlflow grant all on sequences to vandtt;