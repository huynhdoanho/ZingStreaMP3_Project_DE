{{ config(
      materialized = 'view',
      partition_by={
        "field": "ts",
        "data_type": "timestamp",
        "granularity": "day"
      }
  ) }}

SELECT
    fact_streams.userKey AS userKey,
    dim_users.firstName AS firstName,
    dim_users.lastName AS lastName,
    dim_users.gender AS gender,
    dim_users.level AS level,
    dim_users.userId as userId,
    dim_users.currentRow as currentUserRow,

    fact_streams.artistKey AS artistKey,
    dim_artists.latitude AS artistLatitude,
    dim_artists.longitude AS artistLongitude,
    dim_artists.name AS artistName,

    fact_streams.songKey AS songKey,
    dim_songs.duration AS songDuration,
    dim_songs.tempo AS tempo,
    dim_songs.title AS songName,

    fact_streams.dateKey AS dateKey,
    dim_datetime.date AS dateHour,
    dim_datetime.dayOfMonth AS dayOfMonth,
    dim_datetime.dayOfWeek AS dayOfWeek,

    fact_streams.locationKey AS locationKey,
    dim_location.city AS city,
    dim_location.stateName AS state,
    dim_location.latitude AS latitude,
    dim_location.longitude AS longitude,

    fact_streams.ts AS timestamp
FROM
    {{ ref('fact_streams') }}
JOIN
    {{ ref('dim_users') }} ON fact_streams.userKey = dim_users.userKey
JOIN
    {{ ref('dim_songs') }} ON fact_streams.songKey = dim_songs.songKey
JOIN
    {{ ref('dim_location') }} ON fact_streams.locationKey = dim_location.locationKey
JOIN
    {{ ref('dim_datetime') }} ON fact_streams.dateKey = dim_datetime.dateKey
JOIN
    {{ ref('dim_artists') }} ON fact_streams.artistKey = dim_artists.artistKey