/* 
* Cria a view a partir da tabela financeal_market do banco de dados
*/

{{
    config(
        materialized='view'
    )
}}
/* Campos da tabela */
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
/* source('data', 'financial_market') é o nome que está no sources */
FROM {{ source('data', 'financial_market') }}