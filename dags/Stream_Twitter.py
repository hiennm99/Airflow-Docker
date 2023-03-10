from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
from datetime import datetime
from sqlalchemy import create_engine
import pandas as pd
import logging

logger=logging.getLogger()

default_args={
    'owner' : 'me',
    'start_date': datetime.now(),

}
dag =DAG("Stream_Twitter", 
        default_args=default_args, 
        schedule_interval='@once',) 

def ExtractData():
    
    logger.info('Extract data successfully')
def TransformData():
    df=pd.read_parquet('/opt/airflow/dags/data/Twitter/results.parquet',engine='fastparquet')
    
    #Transform data
    df.to_parquet('/opt/airflow/dags/data/Twitter/transformed_data.parquet',engine='fastparquet')
    
    logger.info('Transform data successfully')
def LoadData():
    #Connect to database MySQL
    mysql_user=''
    mysql_password=''
    mysql_host=''
    mysql_port=''
    mysql_db=''
    # mysql_engine=create_engine(f'mysql://{mysql_user}:{mysql_password}@{mysql_host}:{mysql_port}/{mysql_db}')
    print("Connect Successfully")
    
    df=pd.read_parquet('/opt/airflow/dags/data/Twitter/transformed_data.parquet',engine='fastparquet')
    logger.info('Load data successfully')
    

extract = PythonOperator(
    task_id='extract',
    python_callable=ExtractData,
    dag=dag
)

transform = PythonOperator(
    task_id='transform',
    python_callable=TransformData,
    dag=dag
)

load = PythonOperator(
    task_id='load',
    python_callable=LoadData,
    dag=dag
)

extract >> transform >> load