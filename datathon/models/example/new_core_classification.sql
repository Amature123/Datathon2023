
SELECT
    product_style_color as product_id,
    b2c_assortment,
    b2b_assortment,
    total_assortment
FROM {{ source('destination_db', 'new_core_classification') }}