SELECT
    lead_id,
    user_id,
    signup_date,
    deal_stage,
    deal_close_date,
    revenue
FROM
    {{ source('deskbird_data', 'crm') }}