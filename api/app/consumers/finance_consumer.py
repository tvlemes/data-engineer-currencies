"""
Consumer Kafka responsável por consumir os dados financeiros.

Fluxo:

    Kafka
       ↓
    finance.market
       ↓
    Consumer Python
       ↓
    PostgreSQL

Este módulo:

    1. Conecta ao Kafka.
    2. Consome mensagens do tópico finance.market.
    3. Converte o JSON recebido.
    4. Extrai os dados financeiros.
    5. Grava os dados no PostgreSQL.
"""

import json
import logging
import os
import time
from dotenv import load_dotenv

import psycopg2

from kafka import KafkaConsumer

# ============================================================
# CONFIGURAÇÕES .env
# ============================================================
load_dotenv()

# ============================================================
# CONFIGURAÇÕES
# ============================================================
KAFKA_BOOTSTRAP_SERVERS = os.getenv(
    "KAFKA_BOOTSTRAP_SERVERS",
)

KAFKA_TOPIC = os.getenv(
    "KAFKA_TOPIC",
)

KAFKA_GROUP_ID = os.getenv(
    "KAFKA_GROUP_ID",
)


# ============================================================
# POSTGRESQL
# ============================================================
POSTGRES_HOST = os.getenv(
    "POSTGRES_HOST",
)

POSTGRES_PORT = os.getenv(
    "POSTGRES_PORT",
)

POSTGRES_DB = os.getenv(
    "POSTGRES_DB",
)

POSTGRES_USER = os.getenv(
    "POSTGRES_USER",
)

POSTGRES_PASSWORD = os.getenv(
    "POSTGRES_PASSWORD",
)


# ============================================================
# LOGGER
# ============================================================
logging.basicConfig(
    level=logging.INFO,
    format=(
        "%(asctime)s | "
        "%(levelname)s | "
        "%(name)s | "
        "%(message)s"
    ),
)

logger = logging.getLogger("finance-consumer")


# ============================================================
# CONEXÃO POSTGRESQL
# ============================================================
def criar_conexao_postgres():
    """
    Cria uma conexão com o PostgreSQL.

    Returns
    -------
    psycopg2.extensions.connection
        Conexão ativa com o banco.
    """

    while True:

        try:

            conexao = psycopg2.connect(
                host=POSTGRES_HOST,
                port=POSTGRES_PORT,
                database=POSTGRES_DB,
                user=POSTGRES_USER,
                password=POSTGRES_PASSWORD,
            )

            logger.info(
                "Conectado ao PostgreSQL: %s:%s/%s",
                POSTGRES_HOST,
                POSTGRES_PORT,
                POSTGRES_DB,
            )

            return conexao

        except psycopg2.Error as exc:

            logger.warning(
                "PostgreSQL ainda não está disponível: %s",
                exc,
            )

            time.sleep(5)


# ============================================================
# CRIAÇÃO DA TABELA
# ============================================================
def criar_tabela(conexao):
    """
    Cria a tabela financial_market caso ela ainda não exista.
    """

    sql = """
        CREATE TABLE IF NOT EXISTS financial_market (

            id BIGSERIAL PRIMARY KEY,

            source VARCHAR(20) NOT NULL,

            collected_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

            usd_buy NUMERIC(18, 6),
            usd_sell NUMERIC(18, 6),
            usd_variation NUMERIC(18, 6),

            eur_buy NUMERIC(18, 6),
            eur_sell NUMERIC(18, 6),
            eur_variation NUMERIC(18, 6),

            ars_buy NUMERIC(18, 6),
            ars_sell NUMERIC(18, 6),
            ars_variation NUMERIC(18, 6),

            btc_buy NUMERIC(18, 6),
            btc_sell NUMERIC(18, 6),
            btc_variation NUMERIC(18, 6)
        );
    """

    with conexao.cursor() as cursor:

        cursor.execute(sql)

    conexao.commit()

    logger.info(
        "Tabela financial_market verificada/criada."
    )


# ============================================================
# INSERÇÃO DOS DADOS
# ============================================================
def inserir_dados(conexao, dados: dict):
    """
    Extrai os dados financeiros da mensagem Kafka
    e insere uma nova linha no PostgreSQL.
    """

    results = dados.get("results", {})

    currencies = results.get("currencies", {})
    bitcoin = results.get("bitcoin", {})

    usd = currencies.get("USD", {})
    eur = currencies.get("EUR", {})
    ars = currencies.get("ARS", {})
    btc = currencies.get("BTC", {})

    # A API normalmente informa BRL como moeda de origem.
    # Caso o campo não exista ou venha como None,
    # utilizamos BRL como valor padrão.
    source = dados.get("source") or "BRL"

    # Bitcoin pode aparecer em currencies ou em bitcoin,
    # dependendo da estrutura retornada pela API.
    btc_buy = btc.get(
        "buy",
        bitcoin.get("buy")
    )

    btc_sell = btc.get(
        "sell",
        bitcoin.get("sell")
    )

    btc_variation = btc.get(
        "variation",
        bitcoin.get("variation")
    )

    sql = """
        INSERT INTO financial_market (
            source,
            usd_buy,
            usd_sell,
            usd_variation,
            eur_buy,
            eur_sell,
            eur_variation,
            ars_buy,
            ars_sell,
            ars_variation,
            btc_buy,
            btc_sell,
            btc_variation
        )
        VALUES (
            %s,
            %s, %s, %s,
            %s, %s, %s,
            %s, %s, %s,
            %s, %s, %s
        );
    """

    valores = (
        source,

        usd.get("buy"),
        usd.get("sell"),
        usd.get("variation"),

        eur.get("buy"),
        eur.get("sell"),
        eur.get("variation"),

        ars.get("buy"),
        ars.get("sell"),
        ars.get("variation"),

        btc_buy,
        btc_sell,
        btc_variation,
    )

    with conexao.cursor() as cursor:
        cursor.execute(sql, valores)

    conexao.commit()

    logger.info(
        "Dados financeiros gravados no PostgreSQL."
    )


# ============================================================
# CRIAÇÃO DO CONSUMER
# ============================================================

def criar_consumer():

    logger.info(
        "Conectando ao Kafka: %s",
        KAFKA_BOOTSTRAP_SERVERS,
    )

    consumer = KafkaConsumer(

        KAFKA_TOPIC,

        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,

        group_id=KAFKA_GROUP_ID,

        auto_offset_reset="earliest",

        enable_auto_commit=True,

        value_deserializer=lambda value: json.loads(
            value.decode("utf-8")
        ),

    )

    logger.info(
        "Consumer conectado ao tópico: %s",
        KAFKA_TOPIC,
    )

    return consumer


# ============================================================
# CONSUMER PRINCIPAL
# ============================================================

def executar_consumer():

    logger.info(
        "Inicializando Finance Consumer..."
    )

    conexao = criar_conexao_postgres()

    criar_tabela(conexao)

    consumer = criar_consumer()

    logger.info(
        "Aguardando mensagens Kafka..."
    )

    try:

        for mensagem in consumer:

            logger.info(
                "Mensagem recebida: "
                "topic=%s partition=%s offset=%s",
                mensagem.topic,
                mensagem.partition,
                mensagem.offset,
            )

            try:

                dados = mensagem.value

                inserir_dados(
                    conexao,
                    dados,
                )

            except Exception as exc:

                logger.exception(
                    "Erro ao processar mensagem: %s",
                    exc,
                )

                # ------------------------------------------------
                # Se a conexão PostgreSQL tiver sido perdida,
                # tentamos reconectar.
                # ------------------------------------------------

                try:
                    conexao.close()
                except Exception:
                    pass

                conexao = criar_conexao_postgres()

    except KeyboardInterrupt:

        logger.info(
            "Consumer encerrado."
        )

    finally:

        consumer.close()

        conexao.close()


# ============================================================
# EXECUÇÃO
# ============================================================

if __name__ == "__main__":

    executar_consumer()