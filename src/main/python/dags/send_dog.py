from airflow.decorators import dag, task
from datetime import datetime

@dag(
    start_date=None,
    schedule="0 * * * *",
    catchup=False,
)
def send_dog():

    @task
    def run_docker_container():
        import docker
        client = docker.from_env()
        container = client.containers.run("doggy-app", detach=True)
        container.wait()  # Wait for the container to finish
        logs = container.logs().decode('utf-8')
        container.remove()  # Clean up the container
        return logs
    
    @task
    def run_bash():
        import subprocess
        result = subprocess.run(["docker", "run", "--env-file", r"D:\Users\Manu\Documents\Datos\dev\doggy\.env", "doggy-app"], capture_output=True, text=True)
        return result.stdout.strip()



    log_output = run_bash()
        
dag = send_dog()

if __name__ == "__main__":
    conn_path = "connections.yaml"
    variables_path = "variables.yaml"
    my_conf_var = 23    

    dag.test(
        execution_date=datetime.now(),
        conn_file_path=conn_path,
        variable_file_path=variables_path,
        run_conf={"my_conf_var": my_conf_var},
        mark_success_pattern="dog.*",  # regex of task ids to be auto-marked as successful
        use_executor=True
    )
