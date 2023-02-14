import airflow.utils.dates
from airflow import DAG
from airflow.operators.dummy import DummyOperator
from datetime import datetime, timedelta
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash import BashOperator
import crawler_task.crawler as crawler
default_args = {
    'owner': 'qtt',
    'start_date': datetime(2023, 2, 12), 
    # 'depends_on_past': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    # 'catchup': False,
    # 'email_on_retry': False,
    # 'email': ['qtt153759@gmail.com'],
    # 'email_on_failure': True
}
 
dag = DAG(
    dag_id="example_dag_name",
    description="hello airflow",
    # schedule_interval='30 20 * * *',
    # start_date=airflow.utils.dates.days_ago(5),
    default_args=default_args,
    max_active_runs=1
)


# import tasks.hello_task as task
# ticker_crawler = PythonOperator(
#     task_id="ticker_crawler",
#     python_callable=task.crawl,
#     dag=dag)


# ticker_ingest = PythonOperator(
#     task_id="ticker_push_mongo",
#     python_callable=task.test,
#     dag=dag)


test = BashOperator(
    task_id='test',
    bash_command='sudo chmod 777 /opt/airflow || exit 0',
    dag=dag)
crawler_bulk = PythonOperator(
    task_id="crawler_merge",
    python_callable=crawler.create_bulk_data,
    dag=dag)


crawler_url = PythonOperator(
    task_id="crawler_url",
    python_callable=crawler.crawl_url,
    dag=dag)

crawler_post = PythonOperator(
    task_id="crawler_post",
    python_callable=crawler.crawl_post,
    dag=dag)




index_elasticsearch=PythonOperator(
    task_id="index_elasticsearch",
    python_callable=crawler.indexElasticsearch,
    dag=dag)
# test>>crawler_url>>
crawler_url>>crawler_post>>crawler_bulk>>index_elasticsearch




