from datetime import datetime, timedelta

from airflow.plugins_manager import AirflowPlugin


# Utilização {{ macros.ts_macros.ts_format(ts, "%Y") }}
def ts_format(ts, output_format):
    return datetime.strptime(ts[:19], "%Y-%m-%dT%H:%M:%S").strftime(output_format)


# Utilização {{ macros.ts_macros.ts_add(ts, -1) }}
def ts_add(ts, hours):
    ts = datetime.strptime(ts[:19], "%Y-%m-%dT%H:%M:%S")
    if hours:
        ts = ts + timedelta(hours=hours)

    return ts.isoformat()


# Definição da classe de plugin
class TsPlugin(AirflowPlugin):
    name = "ts_macros"
    macros = [ts_format, ts_add]
