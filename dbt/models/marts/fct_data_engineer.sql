/* 
* Cria a tabela a partir da view stg_data_engineer.sql
*/

{{
    config(
        materialized='table'
    )
}}

SELECT
    id,
    collected_at,
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

/* Refenciando a view stg_data_engineer.sql */
FROM {{ ref('stg_data_engineer') }}
