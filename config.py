class Config:
    DEBUG = False
    TESTING = False
    CACHE_TYPE = "SimpleCache"  # You can swap for Redis/Memcached later
    CACHE_DEFAULT_TIMEOUT = 60
