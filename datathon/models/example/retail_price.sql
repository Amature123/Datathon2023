SELECT
    product_id,
    amount as retail_price
FROM {{ source('destination_db', 'retail_price') }}
WHERE TO_DATE(valid_from, 'DD.MM.YYYY') <= CURRENT_DATE
  AND (valid_to = '01.12.9999' OR TO_DATE(valid_to, 'DD.MM.YYYY') > CURRENT_DATE)