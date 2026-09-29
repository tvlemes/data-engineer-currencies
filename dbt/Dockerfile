FROM python:3.12-slim

# Diretório de trabalho do dbt
WORKDIR /usr/app/dbt

# Instala Git
RUN apt-get update \
    && apt-get install -y --no-install-recommends git \
    && rm -rf /var/lib/apt/lists/*

# Instala dbt Core e adapter PostgreSQL
RUN pip install --no-cache-dir \
    dbt-core \
    dbt-postgres \
    psycopg2-binary \
    pytest \
    ruff

# O projeto será montado pelo docker-compose
# através do volume:
# ./dbt:/usr/app/dbt

# Mantém o container executando para permitir:
# docker exec iot-dbt dbt ...
CMD ["tail", "-f", "/dev/null"]