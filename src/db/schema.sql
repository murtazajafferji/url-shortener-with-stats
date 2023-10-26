-- TODO: Replace with appropriate SQL commands to create the appropriate tables

DROP TABLE IF EXISTS urls;

CREATE TABLE urls (
    url_id TEXT PRIMARY KEY,
    redirect_url TEXT NOT NULL,
    auth_token TEXT NOT NULL,
    created_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    expire_time TIMESTAMP
);

CREATE INDEX url_id_and_auth_token_idx ON urls (url_id, auth_token);

-- https://stackoverflow.com/questions/9721804/expire-date-as-default-value-for-timestamp-column
DROP TRIGGER IF EXISTS tr_set_expire_time;

CREATE TRIGGER tr_set_expire_time AFTER INSERT ON urls 
WHEN NEW.expire_time IS NULL
BEGIN
  UPDATE urls SET expire_time = datetime('now', '+30 days') WHERE url_id = NEW.url_id; --TODO: Make expiration configurable
END;

DROP TABLE IF EXISTS stats;

-- TODO: Store this in a NoSQL database
CREATE TABLE stats (
    url_id TEXT,
    ip TEXT NOT NULL,
    visits INTEGER NOT NULL DEFAULT 0
);

CREATE INDEX url_id_and_ip_idx ON stats (url_id, ip);
