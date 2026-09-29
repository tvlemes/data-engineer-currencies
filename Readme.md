# 💰 Finance Data Engineering Pipeline

Projeto de **Engenharia de Dados** desenvolvido para construir um pipeline completo de coleta, processamento, streaming, armazenamento e transformação de dados financeiros.

A solução utiliza uma arquitetura baseada em **APIs, mensageria, banco de dados e orquestração**, permitindo automatizar a coleta de informações do mercado financeiro e disponibilizá-las para posterior análise e transformação.

## 🏗️ Arquitetura

```text
              ┌─────────────────────┐
              │   API Financeira    │
              │     HG Brasil       │
              └──────────┬──────────┘
                         │
                         ▼
              ┌─────────────────────┐
              │      FastAPI        │
              │   REST API / HTTP   │
              └──────────┬──────────┘
                         │
                         ▼
              ┌─────────────────────┐
              │   Apache Kafka      │
              │   finance.market    │
              └──────────┬──────────┘
                         │
                         ▼
              ┌─────────────────────┐
              │ Finance Consumer    │
              │      Python         │
              └──────────┬──────────┘
                         │
                         ▼
              ┌─────────────────────┐
              │     PostgreSQL      │
              │  financial_market   │
              └──────────┬──────────┘
                         │
                         ▼
              ┌─────────────────────┐
              │        dbt          │
              │ Staging + Marts     │
              └──────────┬──────────┘
                         │
                         ▼
              ┌─────────────────────┐
              │ Dados transformados │
              │     para análise    │
              └─────────────────────┘

                        ▲
                        │
                ┌───────┴────────┐
                │ Apache Airflow │
                │  Orquestração  │
                └────────────────┘
```

## 🚀 Tecnologias utilizadas

* 🐍 **Python**
* ⚡ **FastAPI**
* 📨 **Apache Kafka**
* 🐘 **PostgreSQL**
* 🔄 **Apache Airflow**
* 🧱 **dbt**
* 🐳 **Docker**
* 🐙 **Docker Compose**
* 🔌 **REST API**
* 📊 **SQL**
* 🛠️ **Git/GitHub**

## 📡 Coleta de dados

A aplicação utiliza uma API financeira para obter informações relacionadas a:

* 💵 Dólar
* 💶 Euro
* 🇦🇷 Peso argentino
* ₿ Bitcoin
* 📈 Variações de preços
* 💰 Valores de compra e venda

Os dados são coletados através da API desenvolvida com **FastAPI** e posteriormente publicados em um tópico do **Apache Kafka**.

## 📨 Streaming com Kafka

O Kafka atua como camada de mensageria do pipeline.

Os dados financeiros são publicados no tópico:

```text
finance.market
```

Um consumer desenvolvido em Python recebe as mensagens e realiza a persistência dos dados no PostgreSQL.

Essa abordagem permite desacoplar a coleta dos dados do processo de armazenamento.

## 🐘 PostgreSQL

Os dados recebidos pelo consumer são armazenados na tabela:

```text
financial_market
```

Estrutura principal:

```text
financial_market
├── id
├── source
├── collected_at
├── usd_buy
├── usd_sell
├── usd_variation
├── eur_buy
├── eur_sell
├── eur_variation
├── ars_buy
├── ars_sell
├── ars_variation
├── btc_buy
├── btc_sell
└── btc_variation
```

O campo `collected_at` permite registrar o momento em que cada informação foi armazenada.

## 🔄 Transformação com dbt

Após a ingestão no PostgreSQL, o **dbt** é utilizado para organizar e transformar os dados.

A camada de transformação possui:

```text
models/
├── staging/
│   ├── sources.yml
│   └── stg_data_engineer.sql
│
└── marts/
    └── fct_data_engineer.sql
```

### Staging

A camada `staging` representa uma camada intermediária para padronização e preparação dos dados.

```text
financial_market
        │
        ▼
stg_data_engineer
```

### Marts

A camada `marts` disponibiliza os dados transformados para consumo analítico.

```text
stg_data_engineer
        │
        ▼
fct_data_engineer
```

## ⏱️ Orquestração com Airflow

O **Apache Airflow** é utilizado para orquestrar o pipeline.

O DAG é responsável por executar as etapas do processo de forma automatizada, incluindo:

1. Solicitação dos dados financeiros através da API;
2. Publicação dos dados no Kafka;
3. Processamento pelo consumer;
4. Persistência no PostgreSQL;
5. Execução das transformações utilizando dbt.

O pipeline pode ser configurado para execução periódica através de uma expressão cron.

Exemplo:

```text
30min
schedule="*/30 * * * *"
```

Executando o pipeline a cada minuto.

## 🐳 Docker

Toda a infraestrutura do projeto é executada através de containers Docker.

A utilização do Docker permite reproduzir o ambiente de desenvolvimento de forma consistente, isolando os serviços e suas respectivas dependências.

Principais containers:

```text
FastAPI
Kafka
Kafka UI
PostgreSQL
Finance Consumer
Apache Airflow
dbt
pgAdmin
```

## 🔌 API

A API disponibiliza endpoints para consulta dos dados financeiros.

Exemplo:

```http
GET /api/v1/finances
GET /api/v1/bitcoins
GET /api/v1/taxes
```

A API funciona como uma camada de integração entre a fonte de dados financeira e o pipeline de streaming.

## 🎯 Objetivos do projeto

Este projeto foi desenvolvido com foco em práticas de **Data Engineering**, explorando conceitos como:

* ETL/ELT
* Data Pipeline
* Data Ingestion
* Streaming de dados
* Mensageria
* APIs REST
* Data Transformation
* Data Orchestration
* Containerização
* Modelagem de dados
* SQL
* Monitoramento de pipelines
* Arquitetura desacoplada

## 📚 Conceitos de Engenharia de Dados aplicados

O projeto demonstra, na prática, um fluxo completo:

```text
Extract
  ↓
API
  ↓
Ingestion
  ↓
Kafka
  ↓
Processing
  ↓
Consumer
  ↓
Load
  ↓
PostgreSQL
  ↓
Transform
  ↓
dbt
  ↓
Analytics
```

## 📂 Estrutura do projeto

```text
projeto-data-engineer-moeda/
│
├── api/
│   ├── main.py
│   ├── Dockerfile
│   ├── requirements.txt
│   │
│   └── app/
│       ├── models/
│       ├── routers/
│       ├── services/
│       └── consumers/
│
├── airflow/
│   └── dags/
│
├── dbt/
│   ├── models/
│   │   ├── staging/
│   │   └── marts/
│   └── dbt_project.yml
│
├── docker-compose.yml
│
└── README.md
```

## 🔮 Próximas evoluções

Algumas possibilidades de evolução do projeto:

* Dashboard para visualização dos dados;
* Monitoramento do pipeline;
* Data Quality com dbt tests;
* Incremental models no dbt;
* Data Warehouse;
* Histórico de preços;
* Métricas e indicadores financeiros;
* Alertas de falha do pipeline;
* CI/CD;
* Testes automatizados;
* Observabilidade;
* Integração com ferramentas de BI.

## 👨‍💻 Autor

**Thiago Vilarinho Lemes**

👤 Autor: Thiago Vilarinho Lemes <br>
🏠 Home: https://thiagolemes.netlify.app/ \
🔗 LinkedIn: <a href="https://www.linkedin.com/in/thiago-v-lemes-b1232727" target="_blank">Thiago Lemes</a><br>
✉️ e-mail: contatothiagolemes@gmail.com | lemes_vilarinho@yahoo.com.br

---

⭐ Projeto desenvolvido para estudos e demonstração prática de conceitos e ferramentas utilizadas em Engenharia de Dados.
