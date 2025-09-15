from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from datetime import datetime

def load_env_file(filepath):
    env_dict = {}
    with open(filepath) as f:
        for line in f:
            if line.strip() and not line.startswith("#"):
                key, value = line.strip().split("=", 1)
                env_dict[key] = value
    return env_dict

with DAG(
    "enviar_imagen_whatsapp",
    start_date=datetime(2023, 1, 1),
    schedule="*/5 * * * *",  # Cada 5 minutos
    catchup=False,
) as dag:
    
    ejecutar_job = DockerOperator(
        task_id="ejecutar_job",
        image="doggy-app:latest",
        auto_remove='force',
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",  # o la red de tus contenedores
        environment=load_env_file("/opt/airflow/env/.env"),
    )
