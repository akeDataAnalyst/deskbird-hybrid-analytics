SELECT
    wv.session_id,
    wv.page_visited,
    wv.timestamp,
    wv.is_conversion_event,
    wv.conversion_type,
    c.lead_id,
    c.deal_stage,
    c.revenue,
    uc.user_id,         -- Ambiguity fixed by joining uc map
    uc.company_id,
    uc.company_size     -- Crucial dimension added here
FROM
    {{ ref('stg_website_visits') }} AS wv
LEFT JOIN
    {{ ref('stg_crm') }} AS c
ON
    wv.lead_id = c.lead_id
LEFT JOIN
    {{ ref('int_user_company_map') }} AS uc
ON
    wv.user_id = uc.user_id