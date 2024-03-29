import time
import os
from datetime import datetime
import uuid


def get_ttl_hash():
    SECONDS = 3600
    return round(time.time() / SECONDS)


def generate_uuid_and_seed():
    date = datetime.now() - datetime(1970, 1, 1)
    seconds = date.total_seconds()
    seed = round(seconds * 1000) % 1_000_000_000
    game_uuid = uuid.uuid4()
    return game_uuid, seed


def get_env_key(name):
    result = os.environ.get(name)
    if result:
        return result
    
    with open('backend/.env') as f:
        for line in f.readlines():
            key, value = line.split(' ')
            if key == name:
                return value.strip()
            
    return None
