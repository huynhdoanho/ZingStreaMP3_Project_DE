{{ config(materialized = 'table') }}

SELECT {{ dbt_utils.generate_surrogate_key(['latitude', 'longitude', 'city', 'stateName']) }} as locationKey,
*
FROM
    (
        SELECT
            distinct city,
            COALESCE(state_codes.state_code, 'NA') as stateCode,
            COALESCE(state_codes.state_name, 'NA') as stateName,
            lat as latitude,
            lon as longitude
        FROM {{ source('staging', 'listen_events') }}
        LEFT JOIN {{ ref('state_codes') }} on listen_events.state = state_codes.state_code

        UNION ALL

        SELECT
            'NA',
            'NA',
            'NA',
            0.0,
            0.0
    ) as T