"""
Aplicação principal da API. 

Este módulo cria a aplicação FastAPI, 
registra os routers e disponibiliza os endpoints. 

Execução: uvicorn main:app --reload 

URL´s:
Health                                  -> http://127.0.0.1:8000
Consultando HG Brasil atráves desta API -> http://127.0.0.1:8000/api/v1/finance                                  
Swagger                                 -> http://127.0.0.1:8000/docs
ReDoc                                   -> http://127.0.0.1:8000/redoc
Finances                                -> http://127.0.0.1:8000/api/v1/finances
Bitcoins                                -> http://127.0.0.1:8000/api/v1/bitcoins
Taxes                                   -> http://127.0.0.1:8000/api/v1/taxes



"""

from fastapi import FastAPI 
from app.routers.finance import router as finance_router

# ============================================================ 
# FASTAPI 
# ============================================================
app = FastAPI( 
    title="Finance API", 
    description=( 
        "API intermediária para consulta de dados " 
        "financeiros da API HG Brasil." 
    ), 
    version="1.0.0", 
)

# ============================================================ 
# ROUTERS 
# ============================================================ 
app.include_router( 
    finance_router 
)

# ============================================================ 
# HEALTH CHECK 
# ============================================================ 
@app.get( 
    "/", 
    tags=["Health"], 
    summary="Verificar funcionamento da API", 
)
async def health_check(): 
    """ 
    Endpoint simples para verificar se a API está funcionando. 
    """
    return { 
        "status": "online", 
        "service": "Finance API", 
        "version": "1.0.0", 
        "autor": "Thiago Vilarinho Lemes",
        "home": "https://thiagolemes.netlify.app/",
        "github": "https://github.com/tvlemes?tab=repositories",
        "linkedIn": "https://www.linkedin.com/in/thiago-v-lemes-b1232727/",
    }