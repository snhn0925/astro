"""
DAG for Finance Import
"""

from airflow.models import DAG
from pendulum import datetime, timezone
from airflow.operators.python import PythonOperator
from include.financeImport import downloadStockData, stockDataAgg, clearDownloadDir

local_tz = timezone('America/New_York')

# Define the basic parameters of the DAG, like schedule and start_date
dag = DAG(
    dag_id='financeDAG',
    start_date=datetime(2024, 1, 1, tz=local_tz),
    schedule_interval="0 5 * * *",
    catchup=False,
    doc_md=__doc__,
    default_args={"owner": "Snorris", "retries": 3},
    tags=["Gratia Plena"],
)
with dag:
    getStockData = PythonOperator(
        task_id='getStockData',
        python_callable=downloadStockData,
        dag=dag
    )
    
    stockDataResults = PythonOperator(
        task_id='stockDataResults',
        python_callable=stockDataAgg,
        dag=dag
    )
    
    cleanupDownloads = PythonOperator(
        task_id='cleanupDownloads',
        python_callable=clearDownloadDir,
        dag=dag
    )
    
getStockData>>stockDataResults>>cleanupDownloads
