SELECT
    ad_id,
    ad_campaign_name,
    ad_spend,
    impressions,
    clicks,
    click_date
FROM
    {{ source('deskbird_data', 'ad_performance') }}