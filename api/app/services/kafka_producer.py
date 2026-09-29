"""
Producer Kafka responsável pelo envio dos dados financeiros.

Este módulo é responsável por:

    1. Criar a conexão com o Kafka.
    2. Receber os dados financeiros.
    3. Converter os dados para JSON.
    4. Publicar os dados no tópico Kafka.

Quando executado dentro do Docker:

    kafka:29092

Quando executado diretamente no Windows:

    localhost:9092
"""

import json
import logging
import os
from dotenv import load_dotenv

from kafka import KafkaProducer
from kafka.errors import KafkaError

from ..models.currencie import FinanceResponse

# ============================================================
# CARREGA VARIÁVEIS DE AMBIENTE
# ============================================================
load_dotenv()


# ============================================================
# CONFIGURAÇÕES
# ============================================================

# ------------------------------------------------------------
# Endereço do Kafka
# ------------------------------------------------------------
#
# Dentro do Docker:
#
#     kafka:29092
#
# Fora do Docker:
#
#     localhost:9092
#

KAFKA_BOOTSTRAP_SERVERS = os.getenv(
    "KAFKA_BOOTSTRAP_SERVERS",
)


# ------------------------------------------------------------
# Tópico Kafka
# ------------------------------------------------------------

KAFKA_TOPIC = os.getenv(
    "KAFKA_TOPIC",
)


# ============================================================
# LOGGER
# ============================================================

logger = logging.getLogger(__name__)


# ============================================================
# CRIAÇÃO DO PRODUCER
# ============================================================

def criar_producer() -> KafkaProducer:
    """
    Cria e retorna uma instância do KafkaProducer.

    O produtor será responsável por converter
    os dados Python para JSON.
    """

    return KafkaProducer(

        # Endereço do broker Kafka.
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,

        # Converte os dados para JSON.
        value_serializer=lambda value: json.dumps(
            value,
            ensure_ascii=False,
        ).encode("utf-8"),

        # Converte a chave para bytes.
        key_serializer=lambda key: (
            key.encode("utf-8")
            if key is not None
            else None
        ),
    )


# ============================================================
# ENVIO DOS DADOS FINANCEIROS
# ============================================================

def enviar_dados_financeiros(
    dados: FinanceResponse | dict,
) -> bool:
    """
    Envia os dados financeiros para o Kafka.

    Parameters
    ----------
    dados:
        Pode ser um objeto FinanceResponse ou um dicionário.

    Returns
    -------
    bool
        True  -> mensagem enviada com sucesso.
        False -> ocorreu algum erro.
    """

    producer = None

    try:

        # ----------------------------------------------------
        # CONVERSÃO DOS DADOS
        # ----------------------------------------------------
        #
        # Se receber um modelo Pydantic:
        #
        #     FinanceResponse
        #
        # converte para dict utilizando model_dump().
        #
        # Se receber um dict:
        #
        #     {"teste": "kafka"}
        #
        # utiliza o próprio dicionário.
        #

        if isinstance(dados, FinanceResponse):

            dados_dict = dados.model_dump(
                mode="json"
            )

        elif isinstance(dados, dict):

            dados_dict = dados

        else:

            raise TypeError(
                "Os dados precisam ser um FinanceResponse "
                "ou um dicionário."
            )


        # ----------------------------------------------------
        # CRIA O PRODUCER
        # ----------------------------------------------------

        producer = criar_producer()


        # ----------------------------------------------------
        # ENVIA A MENSAGEM
        # ----------------------------------------------------

        future = producer.send(
            KAFKA_TOPIC,
            key="finance",
            value=dados_dict,
        )


        # ----------------------------------------------------
        # AGUARDA CONFIRMAÇÃO DO KAFKA
        # ----------------------------------------------------

        resultado = future.get(
            timeout=10
        )


        # ----------------------------------------------------
        # LOG
        # ----------------------------------------------------

        logger.info(
            "Dados financeiros enviados para Kafka: "
            "topic=%s partition=%s offset=%s",
            resultado.topic,
            resultado.partition,
            resultado.offset,
        )


        return True


    # ========================================================
    # ERRO DO KAFKA
    # ========================================================

    except KafkaError as exc:

        logger.error(
            "Erro ao enviar dados financeiros para Kafka: %s",
            exc,
        )

        return False


    # ========================================================
    # OUTROS ERROS
    # ========================================================

    except Exception as exc:

        logger.exception(
            "Erro inesperado ao enviar dados para Kafka: %s",
            exc,
        )

        return False


    # ========================================================
    # FECHAMENTO
    # ========================================================

    finally:

        if producer is not None:

            producer.flush()
            producer.close()