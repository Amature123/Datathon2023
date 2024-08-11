
SELECT
    product_id,
    product_style,
    product_style_color,
    brand_name,
    color,
    gender,
    size,
    launch_season
FROM {{ source('destination_db', 'productmaster') }}