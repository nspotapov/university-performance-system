import os

database_driver = os.getenv("DATABASE_DRIVER")
database_host = os.getenv("DATABASE_HOST")
database_port = int(os.getenv("DATABASE_PORT"))
database_name = os.getenv("DATABASE_NAME")
database_username = os.getenv("DATABASE_USERNAME")
database_password = os.getenv("DATABASE_PASSWORD")

database_url = ''.join(
    [
        database_driver, "://",
        database_username, ":", database_password, ("@" if database_username or database_password else ""),
        database_host, (":" if str(database_port) else ""), str(database_port), "/", database_name
    ]
)

smtp_host = os.getenv("SMTP_HOST")
smtp_port = os.getenv("SMTP_PORT")
smtp_username = os.getenv("SMTP_USERNAME")
smtp_from = os.getenv("SMTP_FROM")
smtp_password = os.getenv("SMTP_PASSWORD")

otp_code_expired_time = int(os.getenv("OTP_CODE_EXPIRED_TIME", "5"))  # minutes
otp_code_mockup = os.getenv("OTP_CODE_MOCKUP", None)

redis_host = os.getenv("REDIS_HOST")
redis_port = int(os.getenv("REDIS_PORT"))
redis_username = os.getenv("REDIS_USERNAME")
redis_password = os.getenv("REDIS_PASSWORD")
redis_db = int(os.getenv("REDIS_DB", "0"))

jwt_algorithm = os.getenv("JWT_ALGORITHM", "HS256")
jwt_secret_key = os.getenv("JWT_SECRET_KEY")
jwt_token_location = ["headers", "cookies", "query"]
