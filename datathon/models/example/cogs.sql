SELECT 
  product_id,
  amount
FROM {{source('destination_db','cogs')}}
