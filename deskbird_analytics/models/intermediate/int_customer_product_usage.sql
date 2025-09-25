SELECT
    pu.event_id,
    pu.event_name,
    pu.event_timestamp,
    uc.user_id,
    uc.company_id,
    uc.company_size     -- Crucial dimension added here
FROM
    {{ ref('stg_product_usage') }} AS pu
JOIN
    {{ ref('int_user_company_map') }} AS uc
ON
    pu.user_id = uc.user_id