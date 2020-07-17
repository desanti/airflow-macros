from datetime import datetime

from airflow import DAG
from airflow.operators.bash_operator import BashOperator

default_args = {
    "owner": "OWNER",
    "depends_on_past": False,
    "email": "EMAIL@EXAMPLE.COM",
    "start_date": datetime(2020, 7, 17),
}


def ts_format(ts, output_format):
    return datetime.strptime(ts[:19], "%Y-%m-%dT%H:%M:%S").strftime(output_format)


dag = DAG(
    "use_user_defined_macros_dag",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval=None,
    catchup=False,
    user_defined_macros={"ts_format": ts_format},
)


get_year = BashOperator(
    task_id="get_year", bash_command='echo "{{ ts_format(ts, "%Y") }}"', dag=dag
)
