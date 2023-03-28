# import the libraries
from datetime import timedelta
# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG 
# Operators; we need this to write tasks!
from airflow.operators.bash_operator import BashOperator 
# This makes scheduling easy
from airflow.utils.dates import days_ago

# Define DAG arguments
default_args = {
    'owner': 'vins',
    'start_date': days_ago(0),
    'email': ['managbanagmelvin6@gmail.com'],
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 1,
    'retry_delay': timedelta(seconds=3),
}

# Define DAG
dag = DAG(
    'proces_web_log',
    schedule_interval=timedelta(days=1),
    default_args=default_args,
    description='To process web log',
)


# Define task

# Task 1
extract_data = BashOperator(
    task_id= 'extracting_data',
    bash_command= 'cut -d" " -f1 /home/project/airflow/dags/capstone/accesslog.txt >  \
        /home/project/airflow/dags/capstone/extracted_data.txt',
    dag=dag,
)


# Task 2
transform_data = BashOperator(
    task_id = 'transforming_data',
    bash_command = 'grep -v "198.46.149.143" /home/project/airflow/dags/capstone/extracted_data.txt > \
        /home/project/airflow/dags/capstone/transformed_data.txt',
    dag=dag,
)


# Task 3
load_data = BashOperator(
    task_id='loading_the_data',
    bash_command='tar -cf /home/project/airflow/dags/capstone/weblog.tar \
        /home/project/airflow/dags/capstone/transformed_data.txt',
    dag=dag,
)

# Task pipeline
extract_data >> transform_data >> load_data
