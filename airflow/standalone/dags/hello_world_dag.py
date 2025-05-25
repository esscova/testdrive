# ---
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta # Importar timedelta, se for usar em schedule
#---

# argumentos padrão para as tarefas aplicados a todas as tarefas na DAG
default_args = {
    'owner': 'admin',
    'depends_on_past': False, # Não depende de execuções anteriores para rodar
    'email_on_failure': False, # Não envia e-mail em caso de falha
    'email_on_retry': False,   # Não envia e-mail em caso de retry
    'retries': 1,              # Tenta reexecutar a tarefa 1 vez em caso de falha
    'retry_delay': timedelta(minutes=5), # Espera 5 minutos antes de reexecutar
}

# Criação do DAG
with DAG(
    dag_id='hello_world_dag', # Mudei o ID para diferenciar do anterior
    start_date=datetime(2025, 5, 24), # Definindo start_date para hoje
    schedule='@daily',                # executa diariamente
    default_args=default_args,
    catchup=False,                    # Evita execuções retroativas para datas passadas
    tags=['exemplo', 'saudacao'],
) as dag:

    # Tarefa 1: Imprime a data e hora
    tarefa_1 = BashOperator(
        task_id='imprimir_data',
        bash_command='date',
    )

    # Tarefa 2: Imprime "Olá mundo"
    tarefa_2 = BashOperator(
        task_id='ola_mundo',
        bash_command='echo "Olá mundo do Airflow!"',
    )

    # Tarefa 3: Saudação personalizada (usando PythonOperator)
    def saudacao(nome="Mundo"):
        print(f"Olá {nome} do PythonOperator!")
        print(f"Data e hora da execução: {datetime.now()}")

    tarefa_3 = PythonOperator(
        task_id='saudacao_personalizada',
        python_callable=saudacao,
        op_kwargs={'nome': 'Airflow'}, # Argumentos a serem passados para a função python_callable
    )

    # Definição da ordem das tarefas
    tarefa_1 >> tarefa_2 >> tarefa_3
