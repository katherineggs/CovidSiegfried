import pandas as pd
from airflow import DAG
from airflow.contrib.hooks.fs_hook import FSHook
from airflow.contrib.sensors.file_sensor import FileSensor
from airflow.hooks.mysql_hook import MySqlHook
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago

dag = DAG('readCsv', description='Dag to read csv',
          default_args={
              'owner': 'katherine.garcia',
              'depends_on_past': False,
              'max_active_runs': 1,
              'start_date': days_ago(5)
          },
          schedule_interval='0 1 * * *',
          catchup=False)


def processFunc(**kwargs):
    executionDate = kwargs['execution_date']
    print(executionDate)


def processFile(**kwargs):
    # Confirmed
    filepath = f"{FSHook('fs_default').get_path()}/time_series_covid19_confirmed_global.csv"
    dfConfirmed = pd.read_csv(filepath)
    conf = dfConfirmed.melt(id_vars=["Province/State", "Country/Region", "Lat", "Long"],
                            var_name="Date",
                            value_name="Confirmed")
    # to date type
    conf['Date'] = pd.to_datetime(conf['Date'])

    # add new columns
    conf['Year'] = conf['Date'].dt.year
    conf['Month'] = conf['Date'].dt.month
    conf['Day'] = conf['Date'].dt.day

    # Rename columns
    conf = conf.rename(columns={'Long': 'Lon'})

    # Meter a la db
    source = MySqlHook('mydb').get_sqlalchemy_engine()

    with source.begin() as connection:
        conf.to_sql('CovidConfirmed', schema='test', con=connection, if_exists='append', chunksize=2500, index=False)


def processDeaths(**kwargs):
    # # Deaths
    # --- read data
    filepath = f"{FSHook('fs_default1').get_path()}/time_series_covid19_deaths_global.csv"
    dfDeaths = pd.read_csv(filepath)

    # --- order data
    deaths = dfDeaths.melt(id_vars=["Province/State", "Country/Region", "Lat", "Long"],
                           var_name="Date",
                           value_name="Deaths")
    # to date type
    deaths['Date'] = pd.to_datetime(deaths['Date'])

    # add new columns
    deaths['Year'] = deaths['Date'].dt.year
    deaths['Month'] = deaths['Date'].dt.month
    deaths['Day'] = deaths['Date'].dt.day

    # Rename columns
    deaths = deaths.rename(columns={'Long': 'Lon'})

    # Meter a la db
    source = MySqlHook('mydb').get_sqlalchemy_engine()

    with source.begin() as connection:
        deaths.to_sql('CovidDeaths', schema='test', con=connection, if_exists='append', chunksize=2500, index=False)


def processRecovered(**kwargs):
    # # Recovered
    # --- read data
    filepath = f"{FSHook('fs_default2').get_path()}/time_series_covid19_recovered_global.csv"
    dfRecovered = pd.read_csv(filepath)

    # --- order data
    recovered = dfRecovered.melt(id_vars=["Province/State", "Country/Region", "Lat", "Long"],
                                 var_name="Date",
                                 value_name="Recovered")
    # to date type
    recovered['Date'] = pd.to_datetime(recovered['Date'])

    # add new columns
    recovered['Year'] = recovered['Date'].dt.year
    recovered['Month'] = recovered['Date'].dt.month
    recovered['Day'] = recovered['Date'].dt.day

    # Rename columns
    recovered = recovered.rename(columns={'Long': 'Lon'})

    # Meter a la db
    source = MySqlHook('mydb').get_sqlalchemy_engine()

    with source.begin() as connection:
        recovered.to_sql('CovidRecovered', schema='test',
                         con=connection, if_exists='append',
                         chunksize=2500, index=False)

t1 = PythonOperator(
    task_id='inicio_dag',
    dag=dag,
    python_callable=processFunc,
    provide_context=True,
    op_kwargs={
    }
)


sensorConf = FileSensor(task_id="checkConf",
                        dag=dag,
                        poke_interval=10,
                        fs_conn_id="fs_default",
                        filepath="time_series_covid19_confirmed_global.csv",
                        timeout=60)

sensorDeath = FileSensor(task_id="checkDeaths",
                         dag=dag,
                         poke_interval=10,
                         fs_conn_id="fs_default1",
                         filepath="time_series_covid19_deaths_global.csv",
                         timeout=60)

sensorRecov = FileSensor(task_id="checkRecovered",
                         dag=dag,
                         poke_interval=10,
                         fs_conn_id="fs_default2",
                         filepath="time_series_covid19_recovered_global.csv",
                         timeout=60)

processFileConf = PythonOperator(
    task_id='procesarConf',
    dag=dag,
    python_callable=processFile,
    provide_context=True,
    op_kwargs={}
)
processFileDeath = PythonOperator(
    task_id='procesarDeath',
    dag=dag,
    python_callable=processDeaths,
    provide_context=True,
    op_kwargs={}
)
processFileRec = PythonOperator(
    task_id='procesarRec',
    dag=dag,
    python_callable=processRecovered,
    provide_context=True,
    op_kwargs={}
)

sensorConf >> processFileConf >> sensorDeath >> processFileDeath >> sensorRecov >> processFileRec
