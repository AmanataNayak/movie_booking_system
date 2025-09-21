import redis
import pickle

class Cache:
    def __init__(self):
        try:
            self.client: redis.Redis | None = redis.Redis(
                host="localhost",
                port=6379,
                db=0
            )
            self.client.ping()
            print("Successfully connected to Redis.")
        except redis.exceptions.ConnectionError as ce:
            print(f"Could not connect to Redis: {e}")
            self.client = None

    def get(self, key: str):
        if self.client:
            cache_data = self.client.get(key)
            if cache_data:
                print(f"Loading data '{key}' from Redis cache.")
                return pickle.loads(cache_data)

        return None

    def set(self, key: str, value, ttl: int = 3600):
        print(f"Storing data '{key}' in Redis cache.")
        serialized_data = pickle.dumps(value)
        # Set a Time-To-Live (TTL) of 1 hour (3600 seconds) for the cache
        self.client.setex(key, ttl, serialized_data)

