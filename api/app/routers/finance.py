
""" 
    Rotas relacionadas aos dados financeiros. 

    Este módulo define os endpoints FastAPI responsáveis 
    por consultar a API HG Brasil através da camada de serviço. 
"""

from fastapi import APIRouter, HTTPException, status

from ..models.currencie import ( FinanceResponse, Currencie, Bitcoin, Taxes ) 
from ..services.api_hgbrasil import ( HG_BrasilAPIError, obter_dados_financeiros, )
from ..services.kafka_producer import enviar_dados_financeiros

# ============================================================
#  ROUTER 
# ============================================================
router = APIRouter( 
    prefix="/api/v1", 
    tags=["Finance"] 
)

# ============================================================
#  GET /api/v1/finances
#  ============================================================ 
@router.get( 
    "/finances", 
    response_model=FinanceResponse, 
    summary="Consultar dados financeiros", 
    description=( 
        "Consulta a API HG Brasil e retorna os dados " "financeiros validados pelo Pydantic." 
    ), 
    status_code=status.HTTP_200_OK, 
)
async def obter_financeiro() -> FinanceResponse: 
    """ 
    Consulta os dados financeiros da API HG Brasil. 

    Returns: 
        FinanceResponse: 
        Dados financeiros validados. 
        
    Raises: 
        HTTPException: 
            Retorna HTTP 502 quando a API externa apresenta
            algum problema. 
    """

    try:

        # ---------------------------------------------------- 
        # Chama a camada de serviço. 
        # ---------------------------------------------------- 
        dados = await obter_dados_financeiros() 

        # ---------------------------------------------------- 
        # Envia os dados capturados 
        # ---------------------------------------------------- 
        enviar_dados_financeiros(dados)
        
        # ----------------------------------------------------
        # Retorna o modelo Pydantic.
        # ----------------------------------------------------
        return dados

    except HG_BrasilAPIError as exc: 
        # ----------------------------------------------------
        # 502 Bad Gateway 
        # 
        # Significa que nossa API está funcionando, porém 
        # houve um problema ao consultar o serviço externo. 
        # ----------------------------------------------------

        raise HTTPException( 
            status_code=status.HTTP_502_BAD_GATEWAY, 
            detail=str(exc), 
        ) from exc

# ============================================================
#  GET /api/v1/currencies
#  ============================================================ 
@router.get( 
    "/currencies", 
    response_model=Currencie, 
    summary="Consultar Moedas", 
    description=( 
        "Consulta a API HG Brasil e retorna somente os " 
        "dados das moedas."
    ), 
    status_code=status.HTTP_200_OK, 
)
async def obter_moedas() -> Currencie: 
    """ 
    Consulta as moedas da API HG Brasil. 

    Returns: 
        Moedas: 
            Dados das moedas validados pelo Pydantic.
        
    Raises: 
        HTTPException: 
            Retorna HTTP 502 quando a API externa apresenta
            algum problema. 
    """

    try:

        # ---------------------------------------------------- 
        # Chama a camada de serviço. 
        # ---------------------------------------------------- 
        dados = await obter_dados_financeiros() 
        
        # ---------------------------------------------------- 
        # Retorna somente o objeto 'currencies'. 
        # 
        # FinanceResponse 
        #      └── results 
        #         └── currencies 
        # ----------------------------------------------------
        return dados.results.currencies

    except HG_BrasilAPIError as exc: 
        # ----------------------------------------------------
        # 502 Bad Gateway 
        # 
        # Significa que nossa API está funcionando, porém 
        # houve um problema ao consultar o serviço externo. 
        # ----------------------------------------------------

        raise HTTPException( 
            status_code=status.HTTP_502_BAD_GATEWAY, 
            detail=str(exc), 
        ) from exc

# ============================================================
#  GET /api/v1/bitcoins
#  ============================================================ 
@router.get( 
    "/bitcoins", 
    response_model=Bitcoin, 
    summary="Consultar dados Bitcoins", 
    description=( 
        "Consulta a API HG Brasil e retorna somente os " 
        "dados dos bitcoins."
    ), 
    status_code=status.HTTP_200_OK, 
)
async def obter_bitcoin() -> Bitcoin: 

    """ 
    Consulta as moedas da API HG Brasil. 

    Returns: 
        Moedas: 
            Dados das moedas validados pelo Pydantic.
        
    Raises: 
        HTTPException: 
            Retorna HTTP 502 quando a API externa apresenta
            algum problema. 
    """

    try:

        # ---------------------------------------------------- 
        # Chama a camada de serviço. 
        # ---------------------------------------------------- 
        dados = await obter_dados_financeiros() 
        
        # ---------------------------------------------------- 
        # Retorna somente o objeto 'currencies'. 
        # 
        # FinanceResponse 
        #      └── results 
        #         └── currencies 
        # ----------------------------------------------------
        return dados.results.bitcoin

    except HG_BrasilAPIError as exc: 
        # ----------------------------------------------------
        # 502 Bad Gateway 
        # 
        # Significa que nossa API está funcionando, porém 
        # houve um problema ao consultar o serviço externo. 
        # ----------------------------------------------------

        raise HTTPException( 
            status_code=status.HTTP_502_BAD_GATEWAY, 
            detail=str(exc), 
        ) from exc

# ============================================================
#  GET /api/v1/taxes
#  ============================================================ 
@router.get( 
    "/taxes", 
    response_model=list[Taxes], 
    summary="Consultar das Taxas: CDI, Selic, Fator Diário, Selic Diário, CDI Diário", 
    description=( 
        "Consulta a API HG Brasil e retorna somente os " 
        "dados das Taxas: CDI, Selic, Fator Diário, Selic Diário, CDI Diário"
    ), 
    status_code=status.HTTP_200_OK, 
)
async def obter_taxas() -> list[Taxes]: 
    """ 
    Consulta as moedas da API HG Brasil. 

    Returns: 
        Moedas: 
            Dados das moedas validados pelo Pydantic.
        
    Raises: 
        HTTPException: 
            Retorna HTTP 502 quando a API externa apresenta
            algum problema. 
    """

    try:

        # ---------------------------------------------------- 
        # Chama a camada de serviço. 
        # ---------------------------------------------------- 
        dados = await obter_dados_financeiros() 
        
        # ---------------------------------------------------- 
        # Retorna somente o objeto 'currencies'. 
        # 
        # FinanceResponse 
        #      └── results 
        #         └── currencies 
        # ----------------------------------------------------
        return dados.results.taxes

    except HG_BrasilAPIError as exc: 
        # ----------------------------------------------------
        # 502 Bad Gateway 
        # 
        # Significa que nossa API está funcionando, porém 
        # houve um problema ao consultar o serviço externo. 
        # ----------------------------------------------------

        raise HTTPException( 
            status_code=status.HTTP_502_BAD_GATEWAY, 
            detail=str(exc), 
        ) from exc