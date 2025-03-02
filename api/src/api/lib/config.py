from environs import Env

env = Env()

DEBUG: bool = env.bool("DEBUG", False)

SERVER_HOST: str = env.str("SERVER_HOST", "0.0.0.0")
SERVER_PORT: int = env.int("SERVER_PORT", 5000)

DB_URL: str = env.str("DB_URL")
