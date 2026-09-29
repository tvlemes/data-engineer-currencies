# dbt

## Rodando o dbt

1. Primeiramente conferir se os arquivos então
corretos. Dentro da pasta do dbt e com o .venv
rodando digite:
```yaml
dbt debug
```
---
2. Executar os modelos dbt contra o PostgreSQL.
```yaml
dbt run
```
---
3. Execute os testes:
```yaml
dbt test --project-dir "C:\Users\conta\OneDrive\Desktop\Modelo Python\iot-data-engineer\dbt" 

e

dbt test --profiles-dir "C:\Users\conta\OneDrive\Desktop\Modelo Python\iot-data-engineer\dbt"
```
---
4. Verificando o resultado no Postgres:
```yaml
docker compose exec postgres psql -U iot_user -d iot_data -c "\dt"

e

docker compose exec postgres psql -U iot_user -d iot_data -c "\dv"
```
---
5. Consulte os dados

Se você tiver um modelo de staging, podemos consultar:
```yaml
docker compose exec postgres psql -U iot_user -d iot_data -c "SELECT * FROM public.nome_do_modelo LIMIT 10;"
```

E para um modelo de mart:
```yaml
docker compose exec postgres psql -U iot_user -d iot_data -c "SELECT * FROM public.nome_do_mart LIMIT 10;"
```

## Estrutura das pastas e arquivos

Pasta | Descrição
|---|---|
dbt/models | Utilizada para criar as tabelas e views
dbt/models/marts | Pasta que contém os scripts das tabelas que serão criadas.
dbt/models/staging | Pasta que contém os scripts das views que serão criadas.
dbt/profiles.yml | Contém as configurações de conexão com o banco de dados.
dbt/dbt_project.yml | Contém as configurações do dbt. 

**OBS**.: As configurações das pastas dependem de como são declaradas no arquivo dbt_project.yml,
em models.