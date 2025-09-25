SELECT
    event_id,
    user_id,
    event_name,
    event_timestamp
FROM
    {{ source('deskbird_data', 'product_usage') }}