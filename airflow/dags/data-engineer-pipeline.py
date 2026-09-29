"""
====================================================================
                    IOT DATA PIPELINE
====================================================================

Pipeline de Engenharia de Dados IoT

Fluxo:

ESP32
  ↓
FastAPI
  ↓
Kafka
  ↓
PostgreSQL

Orquestração:
Apache Airflow
"""

from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator

# ==================================================================
# CONFIGURAÇÕES GERAIS
# ==================================================================

default_args = {
    "owner": "thiago",

    # A execução atual não depende da execução anterior
    "depends_on_past": False,

    # Número de tentativas adicionais em caso de erro
    "retries": 2,

    # Tempo de espera entre tentativas
    "retry_delay": timedelta(minutes=2),

    # Não enviar e-mails automaticamente
    "email_on_failure": False,
    "email_on_retry": False,
}


# ==================================================================
# DEFINIÇÃO DA DAG
# ==================================================================

with DAG(
    dag_id="data_engineer_pipeline",

    description=(
        "Pipeline Data Engineer"
        "API, Kafka e Postgres"
    ),

    default_args=default_args,

    # ==============================================================
    # EXECUÇÃO AUTOMÁTICA
    # ==============================================================
    #
    # Executa a cada 1min.
   #
   
    schedule="*/30 * * * *",

    # Data inicial da DAG
    start_date=datetime(2026, 9, 29),

    # Não executar períodos antigos
    catchup=False,

    # Impede duas execuções simultâneas da mesma DAG
    max_active_runs=1,

    # Tags para organização no Airflow
    tags=[
        "finance",
        "data",
        "engineer",
        "api",
        "kafka",
        "postgres",
        "dbt",
        "data-engineering",
    ],
) as dag:

    # ==============================================================
    # TASK 1
    # BRONZE → SILVER
    # ==============================================================

    data_engineer_consumer = BashOperator(
        task_id="data_engineer_consumer",

        bash_command="""
            echo "=========================================="
            echo "               CONSUMER"
            echo "=========================================="

            echo "Chamando API financeira..."

            curl -f -X GET \
                http://api:8000/api/v1/finances

            echo ""

            echo "=========================================="
            echo "      CONSUMER CONCLUÍDO"
            echo "=========================================="
        """,

        execution_timeout=timedelta(minutes=15),
    )

    # ==============================================================
    # TASK 2
    # Postgres → dbt
    # ==============================================================

    data_engineer_dbt = BashOperator(
        task_id="data_engineer_dbt",

        bash_command="""
            echo "=========================================="
            echo "               dbt"
            echo "=========================================="

            echo "Chamando dbt..."
            
            docker exec data-engineer-dbt \
                dbt run \
                --project-dir /usr/app/dbt

            echo "=========================================="
            echo "           dbt CONCLUÍDO"
            echo "=========================================="
        """,

        execution_timeout=timedelta(minutes=15),
    )
    
    # ==============================================================
    # DEPENDÊNCIA ENTRE AS TASKS
    # ==============================================================
    data_engineer_consumer >> data_engineer_dbt