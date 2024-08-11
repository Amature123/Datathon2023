
SELECT
    channel_id,
    b2b_b2c,
    store_type,
    region
FROM {{ source('destination_db', 'distribution_channel') }}
