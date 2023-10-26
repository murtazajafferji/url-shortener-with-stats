-- TODO: Replace with appropriate SQL commands to create the appropriate tables
-- TODO: Take "test" suffix as input to avoid code duplication
DROP TABLE IF EXISTS test_urls;

CREATE TABLE test_urls (
    url_id TEXT PRIMARY KEY,
    redirect_url TEXT NOT NULL,
    auth_token TEXT NOT NULL,
    created_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    expire_time TIMESTAMP
);

CREATE INDEX test_url_id_and_auth_token_idx ON test_urls (url_id, auth_token);

-- https://stackoverflow.com/questions/9721804/expire-date-as-default-value-for-timestamp-column
DROP TRIGGER IF EXISTS test_tr_set_expire_time;

CREATE TRIGGER test_tr_set_expire_time AFTER INSERT ON test_urls 
WHEN NEW.expire_time IS NULL
BEGIN
  UPDATE test_urls SET expire_time = datetime('now', '+30 days') WHERE url_id = NEW.url_id; --TODO: Make expiration configurable
END;

DROP TABLE IF EXISTS test_stats;

-- TODO: Store this in a NoSQL database
CREATE TABLE test_stats (
    url_id TEXT,
    ip TEXT NOT NULL,
    visits INTEGER NOT NULL DEFAULT 0
);

CREATE INDEX test_url_id_and_ip_idx ON test_stats (url_id, ip);
