database_url = "sqlite+aiosqlite:///data/database.sqlite"

smtp_host = "smtp.beget.com"
smtp_port = 2525
smtp_username = "university@nspotapov.ru"
smtp_from = "university@nspotapov.ru"
smtp_password = "V%P2WUe2wnwL"

otp_code_expired_time = 5  # minutes

redis_host = "127.0.0.1"
redis_port = 6379
redis_username = None
redis_password = None
redis_db = 0

jwt_algorithm = "HS256"
swt_secret_key = "SECRET_KEY"
jwt_token_location = ["headers", "cookies", "query"]
