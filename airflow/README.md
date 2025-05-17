## Introdução ao Apache Airflow**

### **O que é o Apache Airflow?**

Apache Airflow é uma ferramenta de orquestração de workflows (fluxos de trabalho) open-source, desenvolvida pela comunidade do Apache Software Foundation. Ele permite criar, agendar e monitorar pipelines complexos de tarefas, como:

- Fluxos de ETL (Extração, Transformação e Carga)
- Processamento de dados
- Execução de scripts Python
- Tarefas automatizadas em ambientes de produção

Airflow é amplamente utilizado em cenários de **Data Engineering**, **Machine Learning** e **DevOps**.

---

### **Características Principais do Airflow**

1. **DAGs (Directed Acyclic Graphs)**:
   - Representam fluxos de trabalho estruturados.
   - Definem dependências entre tarefas e controlam a ordem de execução.

2. **Operadores (Operators)**:
   - Unidades básicas de execução.
   - Exemplos:
     - `BashOperator`: Executa comandos Bash.
     - `PythonOperator`: Executa funções Python.
     - `EmailOperator`: Envia e-mails.
     - `BigQueryOperator`: Interage com o Google BigQuery.

3. **Agendamento Flexível**:
   - Usa cron expressões ou intervalos regulares (`@daily`, `@weekly`, etc.).

4. **Monitoramento e Logs**:
   - Interface web intuitiva para visualizar DAGs e logs.
   - Logs detalhados das tarefas executadas.

5. **Escalabilidade**:
   - Suporta desde pequenos projetos até grandes pipelines distribuídos.

---

### **Exemplo de DAG: `primeiro_dag`**

A seguir, apresentamos um exemplo simples de DAG chamado `primeiro_dag`. Este DAG demonstra como criar um fluxo de tarefas usando o Airflow.

#### **Objetivo da DAG**
- Imprimir a data e hora atual.
- Imprimir a mensagem "Olá mundo".
- Executar uma função Python personalizada que imprime uma saudação.

#### **Código da DAG**

```python
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from datetime import datetime

# Argumentos padrão do DAG
default_args = {
    'owner': 'admin',
    'start_date': datetime(2025, 4, 1),
    'schedule_interval': '@daily',
}

# Criação do DAG
dag = DAG(
    dag_id='primeiro_dag',
    default_args=default_args,
)

# Tarefa 1: Imprime a data e hora
tarefa_1 = BashOperator(
    task_id='imprimir_data',
    bash_command='date',
    dag=dag,
)

# Tarefa 2: Imprime "Olá mundo"
tarefa_2 = BashOperator(
    task_id='ola_mundo',
    bash_command='echo "Olá mundo"',
    dag=dag,
)

# Tarefa 3: Saudação personalizada (usando PythonOperator)
def saudacao(nome="Mundo"):
    print(f"Olá {nome}!")

tarefa_3 = PythonOperator(
    task_id='saudacao_personalizada',
    python_callable=saudacao,
    op_kwargs={'nome': 'Airflow'},
    dag=dag,
)

# Definição da ordem das tarefas
tarefa_1 >> tarefa_2 >> tarefa_3
```

---

### **Explicação Passo a Passo**

1. **Importações**:
   - `DAG`: Define o fluxo de trabalho.
   - `BashOperator`: Executa comandos Bash.
   - `PythonOperator`: Executa funções Python.
   - `datetime`: Para definir datas.

2. **Argumentos Padrão (`default_args`)**:
   - `owner`: Responsável pelo DAG.
   - `start_date`: Data de início do DAG.
   - `schedule_interval`: Frequência de execução (diária, neste caso).

3. **Definição do DAG**:
   - `dag_id`: Nome único do DAG.
   - `default_args`: Aplica os argumentos padrão a todas as tarefas.

4. **Tarefas**:
   - **Tarefa 1 (`imprimir_data`)**:
     - Usa o `BashOperator` para executar o comando `date`.
   - **Tarefa 2 (`ola_mundo`)**:
     - Usa o `BashOperator` para imprimir "Olá mundo".
   - **Tarefa 3 (`saudacao_personalizada`)**:
     - Usa o `PythonOperator` para chamar a função `saudacao`.

5. **Ordem das Tarefas**:
   - `tarefa_1 >> tarefa_2 >> tarefa_3`: Define a sequência de execução.

---

### **Como Executar a DAG**

1. **Salve o Código**:
   - Salve o arquivo `primeiro_dag.py` na pasta `dags/` do Airflow.

2. **Inicie o Airflow**:
   ```bash
   airflow db init
   airflow users create \
       --username admin \
       --firstname Admin \
       --lastname User \
       --role Admin \
       --email admin@example.com
   airflow webserver --port 8080
   ```

3. **Acesse a Interface Web**:
   - Abra o navegador em `http://localhost:8080`.
   - Faça login com as credenciais criadas.

4. **Ative o DAG**:
   - Vá para a seção **DAGs**.
   - Localize o DAG `primeiro_dag`.
   - Clique em **Turn On** para ativá-lo.

5. **Force uma Execução Manual**:
   - Clique no DAG `primeiro_dag`.
   - Clique em **Trigger DAG** para rodar manualmente.

6. **Verifique os Logs**:
   - Após a execução, clique nas tarefas individuais (`imprimir_data`, `ola_mundo`, `saudacao_personalizada`).
   - Clique em **View Log** para ver os resultados.

---

### **Resultados Esperados**

- **Tarefa 1 (`imprimir_data`)**:
  ```
  [2025-05-16, 21:16:52] INFO - Thu May 16 21:16:52 UTC 2025
  ```

- **Tarefa 2 (`ola_mundo`)**:
  ```
  [2025-05-16, 21:16:53] INFO - Olá mundo
  ```

- **Tarefa 3 (`saudacao_personalizada`)**:
  ```
  [2025-05-16, 21:16:54] INFO - Olá Airflow!
  ```

---

### **Recursos Adicionais**

- **Documentação Oficial**: [https://airflow.apache.org/docs/](https://airflow.apache.org/docs/)
- **Comunidade**: [Slack do Airflow](https://apache-airflow.slack.com)
- **GitHub**: [https://github.com/apache/airflow](https://github.com/apache/airflow)

### Autor
[Wellington M Santos](https://www.linkedin.com/in/wellington-moreira-santos/)
