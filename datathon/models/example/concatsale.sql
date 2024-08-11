{{ config(materialized='table') }}

{% set schema_name = 'destination_db' %}

{% set table_prefix = 'tt' %} 

{% set number_of_tables = var('nsale') %}  

with concatSale as (
    {% for i in range(0, number_of_tables) %}
        select * from {{ source(schema_name, table_prefix ~ i) }}
        {% if not loop.last %}union all{% endif %}

    {% endfor %}
)

select * from concatSale