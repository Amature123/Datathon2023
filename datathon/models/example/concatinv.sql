{{ config(materialized='table') }}

{% set schema_name = 'destination_db' %}
{% set table_prefix = 'tonkho' %}
{% set number_of_tables = var('ninv') %}

with concatInv as (
    {% for i in range(0, number_of_tables) %}
        select * from {{ source(schema_name, table_prefix ~ i) }}
        {% if not loop.last %}union all{% endif %}
    {% endfor %}
)

select
    {% set columns = adapter.get_columns_in_relation(this) %}
    {% for col in columns if col.name != 'Unnamed: 0' %}
        {{ col.name }}{% if not loop.last %},{% endif %}
    {% endfor %}
from concatInv