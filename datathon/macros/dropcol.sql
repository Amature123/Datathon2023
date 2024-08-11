
{% macro dropcol(source_name, table_name) %}

{% set sql %}
    SELECT 
        {% for col in adapter.get_columns_in_relation(source(source_name, table_name)) -%}
            {% if col.name != "Unnamed: 0" %}
                {{ col.name }}{% if not loop.last %},{% endif %}
            {% endif %}
        {%- endfor %}
    FROM {{ source(source_name, table_name) }}
{% endset %}

{% do log("Column 'Unnamed: 0' has been excluded from table '" ~ table_name ~ "'", info=True) %}

{{ return(sql) }}

{% endmacro %}