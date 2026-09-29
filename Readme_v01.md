# Arquitetura proposta
```yaml
                EXTERNAL
                   │
                   ▼
             ┌─────────────┐
             │ HG Brasil   │
             │    API      │
             └──────┬──────┘
                    │
                    ▼
             ┌─────────────┐
             │  FastAPI    │
             │  Ingestion  │
             └──────┬──────┘
                    │
                    │ JSON
                    ▼
             ┌─────────────┐
             │    Kafka    │
             │             │
             │ topic:      │
             │ finance.    │
             │ currencies  │
             └──────┬──────┘
                    │
                    ▼
             ┌─────────────┐
             │ Kafka       │
             │ Consumer    │
             └──────┬──────┘
                    │
                    ▼
             ┌─────────────┐
             │    MinIO    │
             │             │
             │ Bronze      │
             └──────┬──────┘
                    │
                    ▼
             ┌─────────────┐
             │    Spark    │
             │             │
             │ Silver      │
             │ Gold        │
             └──────┬──────┘
                    │
                    ▼
             ┌─────────────┐
             │ PostgreSQL  │
             │     DW      │
             └─────────────┘


          ┌───────────────────┐
          │      Airflow      │
          │                   │
          │ agenda/orquestra  │
          │ os processos      │
          └───────────────────┘
```
---
## Função de cada componente:
| Componente     | Responsabilidade                                      |
|---|---|
| **HG Brasil**  | Fonte externa dos dados                               |
| **FastAPI**    | Buscar/normalizar os dados e disponibilizar endpoints |
| **Kafka**      | Transportar os eventos financeiros                    |
| **Consumer**   | Consumir mensagens Kafka                              |
| **MinIO**      | Armazenar os dados brutos                             |
| **Airflow**    | Agendar e orquestrar os pipelines                     |
| **Spark**      | Processar grandes volumes                             |
| **dbt**        | Transformações no DW                                  |
| **PostgreSQL** | Camada analítica/DW                                   |
---
## Arquitetura das pastas:
Caminho | Descrição
|---|---|
api/ |  Pasta da API.
api/.venv | Utilizada para testes, pois o Docker ainda não foi criado. EXCLUÍDO PARA LIBERAR ESPAÇO.
api/main.py | Aplicação principal, utilizada para testes, pois o Docker ainda não foi criado. 
api/Dockerfile | Dockerfile do container da API
api/app/models/currencie.py | Contém a modelagem dos dados a serem capturados.
api/app/routers/finance.py | Rotas relacionadas aos dados financeiros. 
api/app/services/api_hgbrasil.py | Serviço de integração com a API HG Brasil Finance. 
api/app/services/kafka_producer.py | Producer Kafka responsável pelo envio dos dados financeiros. NÃO UTILIZADO.
api/app/services/kafka | Pasta do Kafka
api/app/cosumers/finance_consumer.py | Script responsável por criar a tabela financial_market e inserir os dados no Postgres dos extraídos do site HG Brasil na URL http://127.0.0.1:8000/api/v1/finances 
dbt | Pasta que contém as configurações do dbt.
---
## Compilando Dockerfile e docker-compose.yml
Validando o docker-compose.yml
```yaml
docker compose config
```

**Dockerfile**\
```yaml
docker build -t data-engineer-api:1.0 .

ou

docker compose build --no-cache api
```

**docker-compose.yml**
```yaml
docker compose up -d

para compilar e subir tudo

docker compose up -d --build
```
**OBS.:** caso venha ocorrer erros que não encontra as libs limpa o cache do **Docker Desktop**, exclua as Imagens, os Volumes, e os Builds.
---
Para entrar dentro do Docker
```
docker exec -it data-engineer-dbt sh
```
---

 
## Criando o comsumer.py
Poderia colocar o Consumer dentro do próprio serviço Kafka, mas eu não é recomendado misturar os dois.\
A diferença é de responsabilidade.
O Kafka é o mensageiro/broker. O finance_consumer.py é a aplicação que lê as mensagens.

```yaml
                 Kafka
          ┌─────────────────┐
          │                 │
FastAPI → │ finance.market  │
          │                 │
          └────────┬────────┘
                   │
                   ▼
          finance_consumer.py
                   │
                   ▼
              PostgreSQL
```

O mais adequado para o projeto Data Engineering é:
```yaml
                    ┌──────────────────┐
                    │      FastAPI     │
                    │     Producer     │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │      KAFKA       │
                    │                  │
                    │ finance.market   │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │     CONSUMER     │
                    │ finance_consumer │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │   PostgreSQL     │
                    │  finance_data    │
                    └──────────────────┘
```

Por que isso é melhor?

Porque depois você pode ter vários consumidores do mesmo tópico:
```yaml
                     finance.market
                           │
              ┌────────────┼────────────┐
              │            │            │
              ▼            ▼            ▼
          Consumer      Consumer      Consumer
          PostgreSQL    Analytics     Data Lake
```

Por exemplo, amanhã podemos fazer:
```yaml
Kafka
  │
  ├──→ PostgreSQL
  │
  ├──→ MinIO
  │
  └──→ Spark
```

E tem outra vantagem importante

Se o PostgreSQL cair:
```yaml
Kafka
  ↓
Consumer
  X
PostgreSQL
```
o Kafka continua armazenando as mensagens e o Consumer pode voltar a processá-las depois.\
Se colocássemos tudo junto no serviço Kafka, perderíamos essa separação.