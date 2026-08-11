"""KurupDevs - Config Module"""
import os

try:
    from environs import Env
    env = Env()
    env.read_env("./.env")
except (FileNotFoundError, ImportError):
    env = None

def _get(key, default=None):
    """Retrieve config value from env with fallback."""
    val = os.getenv(key)
    if val is not None:
        return val
    if env is not None:
        try:
            return env.str(key)
        except Exception:
            pass  # intentionally suppressed
    return default

api_id = int(_get("API_ID", "0"))
api_hash = _get("API_HASH", "")
session_string = _get("SESSION_STRING", "")
db_type = _get("DATABASE_TYPE", "sqlite").lower()
db_url = _get("DATABASE_URL", "")
db_name = _get("DATABASE_NAME", "kurupdevs")
weather_api_key = _get("WEATHER_API_KEY", "")
gemini_key = _get("GEMINI_KEY", "")
openai_key = _get("OPENAI_KEY", "")
pm_limit = int(_get("PM_LIMIT", "4"))
prefix = _get("PREFIX", ".")
port = int(_get("PORT", "8000"))
quotes_api = "https://quotes-o042.onrender.com/generate"