CREATE TABLE IF NOT EXISTS staging.listen_events (
    artist VARCHAR(255),
    song VARCHAR(255),
    duration DOUBLE PRECISION,
    ts TIMESTAMP,
    sessionid BIGINT,
    auth VARCHAR(255),
    level VARCHAR(255),
    itemInSession BIGINT,
    city VARCHAR(255),
    zip BIGINT,
    state VARCHAR(255),
    userAgent VARCHAR(255),
    lon DOUBLE PRECISION,
    lat DOUBLE PRECISION,
    userId BIGINT,
    lastName VARCHAR(255),
    firstName VARCHAR(255),
    gender VARCHAR(255),
    registration BIGINT,
    month BIGINT,
    day BIGINT,
    hour VARCHAR(255)
);