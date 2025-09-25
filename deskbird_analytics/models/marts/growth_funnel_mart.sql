SELECT
    EXTRACT(MONTH FROM ffe.timestamp) AS event_month,
    ffe.company_id,
    ffe.company_size, -- Direct, non-ambiguous column from intermediate model
    SUM(CASE WHEN ffe.is_conversion_event THEN 1 ELSE 0 END) AS total_conversions,
    COUNT(DISTINCT ffe.user_id) AS unique_visitors,
    COUNT(DISTINCT ffe.lead_id) AS total_leads,
    SUM(CASE WHEN ffe.deal_stage = 'Won' THEN 1 ELSE 0 END) AS total_customers,
    SUM(ffe.revenue) AS total_revenue
FROM
    {{ ref('int_full_funnel_events') }} AS ffe
GROUP BY 1, 2, 3