TAG_METADATA = [
    {"name": "v1", "description": "Operations with trading results v1"},
    {
        "name": "healthz",
        "description": "Standard service health check",
    },
]

TITLE = "FastAPI trading results API"

DESCRIPTION = "API for obtaining filtered trading results from a database"

VERSION = "0.0.1"

ERROR_MAPS = {
    "postgres": "PostgreSQL connection failed",
    "redis": "Redis connection failed",
}
