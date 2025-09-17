from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from datetime import datetime

with DAG(
    "enviar_imagen_whatsapp",
    start_date=datetime(2023, 1, 1),
    schedule="*/5 * * * *",  # Cada 5 minutos
    catchup=False,
) as dag:
    
    ejecutar_job = DockerOperator(
        task_id="ejecutar_job",
        image="doggy-producer:latest",
        auto_remove='force',
        docker_url="unix://var/run/docker.sock",
        network_mode="doggy_doggy-net"
    )
