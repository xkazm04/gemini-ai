import redis
from pydantic import BaseModel
import os
from rq import Queue
key = os.environ.get("REDIS_KEY")
redis_url = os.environ.get("REDIS_URL")

r = redis.Redis(
    host=redis_url,
    port=31713,
    password=key,
    decode_responses=True
)

task_queue = Queue(name="user_queue",connection=r)

class User(BaseModel):
    username: str
    email: str
    role: str
    password: str
    
    
def create_redis_user(data: User):
    r.set(data.username, data.json())
    return r.get(data.username)


def queue_new_user(data: User):
    task_queue.enqueue(create_redis_user, data)
    return data.username