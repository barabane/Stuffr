import json

from pydantic import BaseModel
from redis.asyncio import Redis, from_url


class RedisCache:
    async def init(self, url: str):
        self.redis: Redis = await from_url(url, encoding='utf-8', decode_responses=True)

    async def set(self, key: str, value, expire: int = 60):
        key = f'cached:{key}'

        if isinstance(value, list):
            result = []
            for item in value:
                if isinstance(item, BaseModel):
                    result.append(json.dumps(item.model_dump()))
                else:
                    result.append(json.dumps(item))
            await self.redis.set(key, json.dumps(result), ex=expire)
        else:
            await self.redis.set(key, json.dumps(value), ex=expire)

    async def get(self, key: str):
        result = await self.redis.get(f'cached:{key}')
        if result:
            if isinstance(json.loads(result), list):
                return [json.loads(item) for item in json.loads(result)]
            return json.loads(result)
        return None

    async def delete(self, key: str):
        await self.redis.delete(f'cached:{key}')

    async def close(self):
        await self.redis.close()


redis_cache = RedisCache()
