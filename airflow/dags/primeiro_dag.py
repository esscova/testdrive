from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator 
from datetime import datetime

# argumentos do DAG
default_args = {
    'owner': 'admin',
    'start_date': datetime(2025, 4, 1),
    'schedule_interval': '@daily',
}

# DAG
dag = DAG(
    dag_id='primeiro_dag',
    default_args=default_args,
)

# task 1: imprime data e hora
tarefa_1 = BashOperator(
    task_id='imprimir_data',
    bash_command='date',
    dag=dag,
)

# task 2: imprime "Olá mundo"
tarefa_2 = BashOperator(
    task_id='ola_mundo',
    bash_command='echo "Olá mundo"',
    dag=dag,
)

# task 3: saudação personalizada (PythonOperator)
def saudacao(nome="Mundo"):
    print(f"Olá {nome}!")

tarefa_3 = PythonOperator(
    task_id='saudacao_personalizada',
    python_callable=saudacao,        # função a ser executada
    op_kwargs={'nome': 'Airflow'},   # argumentos da função
    dag=dag,
)

# ordenar tasks
tarefa_1 >> tarefa_2 >> tarefa_3
