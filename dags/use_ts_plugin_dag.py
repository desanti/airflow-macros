from datetime import datetime

from airflow import DAG
from airflow.operators.bash_operator import BashOperator

default_args = {
    "owner": "OWNER",
    "depends_on_past": False,
    "email": "EMAIL@EXAMPLE.COM",
    "start_date": datetime(2020, 7, 17),
}


dag = DAG(
    "use_ts_plugin_dag",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval=None,
    catchup=False,
)


get_year = BashOperator(
    task_id="get_year",
    bash_command='echo "{{ macros.ts_macros.ts_format(ts, "%Y") }}"',
    dag=dag,
)

sum_10_hours = BashOperator(
    task_id="sum_10_hours",
    bash_command='echo "{{ macros.ts_macros.ts_add(ts, 10) }}"',
    dag=dag,
)
