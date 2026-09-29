""" 
Serviço de integração com a API HG Brasil Finance. 

Este módulo é responsável por: 
    1. Fazer a requisição HTTP para a API HG Brasil. 
    2. Utilizar HTTP assíncrono através do httpx.AsyncClient. 
    3. Receber o JSON retornado pela API. 
    4. Validar os dados utilizando o modelo FinanceResponse. 
    5. Retornar um objeto FinanceResponse já validado.

A camada de serviço fica responsável pela comunicação com a API externa. 
A camada de rota (router) não precisa conhecer detalhes de HTTP, 
URL ou autenticação da HG Brasil. 
"""

import httpx
from ..models.currencie import FinanceResponse
from dotenv import load_dotenv
import os


# ================================================
# # CONFIGURAÇÕES 
# ================================================
load_dotenv()
HG_BRASIL_URL = os.getenv('HG_BRASIL_URL') 
HG_BRASIL_API_KEY = os.getenv('HG_BRASIL_API_KEY')

# Tempo máximo de espera da requisição. #
# 
# connect: tempo máximo para estabelecer conexão. 
# read: tempo máximo para receber a resposta. 
# write: tempo máximo para enviar os dados. 
# pool: tempo máximo para obter uma conexão. 
# 
# Os valores estão em segundos. 
TIMEOUT = httpx.Timeout( 
    connect=10.0, 
    read=15.0, 
    write=10.0, 
    pool=10.0, 
)


# ============================================================ 
# EXCEÇÕES 
# ============================================================ 
class HG_BrasilAPIError(Exception):
    """ Exceção utilizada quando ocorre algum problema 
        na comunicação com a API HG Brasil. 
    """ 
    pass

# ============================================================ 
# SERVIÇO 
# ============================================================ 
async def obter_dados_financeiros() -> FinanceResponse:
    """ 
        Consulta a API HG Brasil Finance. 
        
        Returns: 
            FinanceResponse: 
                Dados financeiros validados pelo Pydantic. 
            
        Raises: 
            HG BrasilAPIError: 
                Quando ocorre algum erro na comunicação, resposta 
                HTTP inválida ou erro de validação. 
    """

    # -------------------------------------------------------- 
    # Parâmetros enviados para a API HG Brasil 
    # --------------------------------------------------------
    params = { 
        "key": HG_BRASIL_API_KEY, 
    }

    try:
        # ---------------------------------------------------- 
        # Cria um cliente HTTP assíncrono 
        # ----------------------------------------------------
        async with httpx.AsyncClient( 
            timeout=TIMEOUT 
        ) as client:

            # ------------------------------------------------ 
            # Faz a requisição GET 
            # ------------------------------------------------ 
            response = await client.get( 
                HG_BRASIL_URL, 
                params=params, 
            )

            # ------------------------------------------------ 
            # Verifica erros HTTP 
            # Exemplos: 
            # 400 
            # 401 
            # 403 
            # 404 
            # 500 
            # ------------------------------------------------ 
            response.raise_for_status()

            # ------------------------------------------------ 
            # Converte a resposta para Python dict 
            # ------------------------------------------------ 
            data = response.json()

    # -------------------------------------------------------- 
    # Erros de conexão 
    # -------------------------------------------------------- 
    except httpx.TimeoutException as exc: 
        raise HG_BrasilAPIError( 
            f"Tempo limite excedido ao consultar a API HG Brasil." 
        ) from exc

    except httpx.RequestError as exc: 
        raise HG_BrasilAPIError( 
            f"Erro de comunicação com a API HG Brasil: {exc}" 
        ) from exc

    # -------------------------------------------------------- 
    # Erros HTTP 
    # --------------------------------------------------------
    except httpx.HTTPStatusError as exc: 
        raise HG_BrasilAPIError( 
            "A API HG Brasil retornou um erro HTTP "
              f"{exc.response.status_code}."
        ) from exc 
    
    # -------------------------------------------------------- 
    # Erros relacionados ao JSON 
    # --------------------------------------------------------
    except ValueError as exc: 
        raise HG_BrasilAPIError( 
            "A API HG Brasil retornou uma resposta que " 
            "não pôde ser interpretada como JSON."
        ) from exc
    
    # ======================================================== 
    # VALIDAÇÃO COM PYDANTIC 
    # ======================================================== 
    try:
        # ---------------------------------------------------- 
        # Converte o dicionário retornado pela API para # o modelo FinanceResponse. 
        # Aqui acontece a validação automática do Pydantic. 
        # ---------------------------------------------------- 
        resultado = FinanceResponse.model_validate(data)
    except Exception as exc:
        raise HG_BrasilAPIError( 
            "A resposta da API HG Brasil não corresponde " 
            "ao modelo FinanceResponse." 
        ) from exc

    # -------------------------------------------------------- 
    # Retorna o objeto validado 
    # -------------------------------------------------------- 
    return resultado