import time
import datetime
import uuid


def get_ttl_hash():
    SECONDS = 3600
    return round(time.time() / SECONDS)



def generate_uuid_and_seed():
    date = datetime.utcnow() - datetime(1970, 1, 1)
    seconds = date.total_seconds()
    seed = round(seconds * 1000) % 1_000_000_000
    game_uuid = uuid.uuid4()
    return game_uuid, seed
