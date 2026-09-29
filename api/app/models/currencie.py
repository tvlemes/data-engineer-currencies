"""
Modelos de dados da API HG Brasil Finance.

Este arquivo define os modelos Pydantic utilizados
para representar os dados retornados pela API externa.

Documentação:
https://console.hgbrasil.com/documentation/finance
"""

from typing import List, Optional

from pydantic import BaseModel, Field


# ============================================================
# Currencie(MOEDA) - MODEL
# ============================================================
class CurrencieExchange(BaseModel):
    """
    Representa uma moeda retornada pela API HG Brasil.
    """

    name: str = Field(
        ...,
        description="Nome da moeda"
    )

    buy: Optional[float] = Field(
        None,
        description="Valor de compra"
    )

    sell: Optional[float] = Field(
        None,
        description="Valor de venda"
    )

    variation: Optional[float] = Field(
        None,
        description="Variação percentual"
    )


# ============================================================
# Currencie(MOEDA) - LISTA PERMITIDA
# ============================================================
class Currencie(BaseModel):
    """
    Representa o conjunto de moedas retornadas pela API.

    O HG Brasil utiliza o código ISO da moeda como chave
    dentro de 'currencies'.
    """

    source: str = Field(
        ...,
        description="Moeda base utilizada na cotação"
    )

    USD: Optional[CurrencieExchange] = None # MoedaMercado - é herdado dos parâmetros da classe MoedaMercado
    EUR: Optional[CurrencieExchange] = None
    # GBP: Optional[CurrencieExchange] = None
    ARS: Optional[CurrencieExchange] = None
    # CAD: Optional[MoedaMercado] = None
    # AUD: Optional[MoedaMercado] = None
    # JPY: Optional[MoedaMercado] = None
    # CNY: Optional[MoedaMercado] = None
    BTC: Optional[CurrencieExchange] = None

# ============================================================
# BITCOIN EXCHANGE - MODEL
# ============================================================
class BitcoinExchange(BaseModel):
    """
    Representa a cotação do Bitcoin em uma exchange.
    """

    name: str = Field(
        ...,
        description="Nome da exchange"
    )

    format: List[str] = Field(
        ...,
        description="Código da moeda e idioma"
    )

    last: Optional[float] = Field(
        None,
        description="Última cotação"
    )

    buy: Optional[float] = Field(
        None,
        description="Valor de compra"
    )

    sell: Optional[float] = Field(
        None,
        description="Valor de venda"
    )

    variation: Optional[float] = Field(
        None,
        description="Variação percentual"
    )

# ============================================================
# BITCOIN - LISTA PERMITIDA
# ============================================================
class Bitcoin(BaseModel):
    """
    Cotações do Bitcoin nas principais exchanges.
    """

    blockchain_info: Optional[BitcoinExchange] = None

    bitstamp: Optional[BitcoinExchange] = None

    # foxbit: Optional[BitcoinExchange] = None

    # mercadobitcoin: Optional[BitcoinExchange] = None

# ============================================================
# TAXES
# ============================================================
class Taxes(BaseModel):

    date: str = Field(
        ...,
        description="Data captura"
    )

    cdi: float = Field(
        ...,
        description="Taxa do CDI - Certificado de Depósito Interbancário"
    ),

    selic: float = Field(
        ...,
        description="Taxa do Selic - Taxa Básica de Juros"
    ),

    daily_factor: float = Field(
        ...,
        description="Fator Diário"
    )

    selic_daily: float = Field(
        ...,
        description="Taxa do Selic Diário"
    ),
    
    cdi_daily: float = Field(
        ...,
        description="Taxa do CDI Diário"
    )

# ============================================================
# RESULTS
# ============================================================
class Results(BaseModel):
    """
    Dados financeiros retornados pela API HG Brasil.
    """

    currencies: Currencie

    available_sources: List[str]

    bitcoin: Bitcoin

    taxes: list[Taxes]

# ============================================================
# RESPOSTA PRINCIPAL
# ============================================================
class FinanceResponse(BaseModel):
    """
    Resposta principal da API HG Brasil Finance.
    """

    by: str = Field(
        ...,
        description="Tipo da consulta realizada"
    )

    valid_key: bool = Field(
        ...,
        description="Indica se a chave da API é válida"
    )

    results: Results

    execution_time: float = Field(
        ...,
        description="Tempo de execução da consulta"
    )

    from_cache: bool = Field(
        ...,
        description="Indica se a resposta veio do cache"
    )
