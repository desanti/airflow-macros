# airflow-macros

Exemplo para a utilização de macros com duas abordagens, a primeira é a utilização de plugin, enquanto a segunda é a utilização de user_defined_macros.

## Plugin

Implementação e utilização de plugin para gerar macros genéricas. Quando feita a macro via plugin é possível utilizar em qualquer DAG do Airflow.

### Implementação do Plugin

Para implementar o plugin é necessário herdar da classe `AirflowPlugin`:

```python
class TsPlugin(AirflowPlugin):
    name = "ts_macros"
    macros = [ts_format, ts_add]
```

Neste exemplo, foi criado o plugin com nome `ts_macros`, e com as macros `ts_format` e `ts_add`, conforme código abaixo:

```python
def ts_format(ts, output_format):
    return datetime.strptime(ts[:19], "%Y-%m-%dT%H:%M:%S").strftime(output_format)

def ts_add(ts, hours):
    ts = datetime.strptime(ts[:19], "%Y-%m-%dT%H:%M:%S")
    if hours:
        ts = ts + timedelta(hours=hours)

    return ts.isoformat()
```

### Forma de utilização

Na DAG é possível utilizar as macros de forma bem similar as já disponíveis pelo Airflow:

```python
sum_10_hours = BashOperator(
    task_id="sum_10_hours",
    bash_command='echo "{{ macros.ts_macros.ts_add(ts, 10) }}"',
    dag=dag,
)
```

Para que a macro seja executada corretamente:

- utiliza a estrutura padrão dos macros do Airflow: `{{ macros. }}`.
- o nome do plugin: `ts_macros`.
- a macro que será executada e seus parâmetros: `ts_add(ts, 10)`.

### Configuração do Airflow

É necessário que o Airflow seja configurado para que os plugins funcionem. Para isso é necessário editar o arquivo `airflow.cfg`, e procurar pela chave `plugins_folder`:

```bash
# Where your Airflow plugins are stored
plugins_folder = /home/user/airflow/plugins
```

Você pode alterar o diretório onde serão armazenados os plugins, ou, colocá-los no diretório já configurado.

*OBS*: não é recomendável colocar no mesmo diretório das DAGs.


## User Defined Macros

Essas macros são funções dentro da própria DAG, ou em arquivos específicos para as mesmas, e não é necessário realizar a configuração de um plugin.

```python
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

```

O primeiro passo é a implementação de uma função, neste caso `ts_format`. Posteriormente, é necessário configurar o parâmetro `user_defined_macros`:

```python
user_defined_macros={"ts_format": ts_format},
```

E, então a utilização, onde a chamada da macro é a `key` do dicionário passado no parâmetro `user_defined_macros`.

```python
{{ ts_format(ts, "%Y") }}
```
