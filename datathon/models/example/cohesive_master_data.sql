{{ config(materialized='table') }}

WITH product_base AS (
    SELECT * FROM {{ ref('productmaster') }}
),
latest_cogs AS (
    SELECT * FROM {{ ref('cogs') }}
),
current_retail_price AS (
    SELECT * FROM {{ ref('retail_price') }}
),
product_classification AS (
    SELECT * FROM {{ ref('new_core_classification') }}
),
product_channel as (
  SELECT 
      pb.product_id,
      pb.product_style,
      pb.product_style_color,
      pb.brand_name,
      pb.color,
      pb.gender,
      pb.size,
      pb.launch_season,
      lc.amount AS current_cost_price,
      crp.retail_price AS current_retail_price,
      pc.b2c_assortment,
      pc.b2b_assortment,
      pc.total_assortment
  FROM 
      product_base pb
  LEFT JOIN 
      latest_cogs lc ON pb.product_id = lc.product_id
  LEFT JOIN 
      current_retail_price crp ON pb.product_id = crp.product_id
  LEFT JOIN 
      product_classification pc ON pb.product_id = pc.product_id
)

SELECT 
    *
FROM 
    product_channel 

