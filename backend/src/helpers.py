import os
from datetime import datetime
import uuid
from dotenv import load_dotenv

load_dotenv()


def generate_uuid_and_seed():
    date = datetime.now() - datetime(1970, 1, 1)
    seconds = date.total_seconds()
    seed = round(seconds * 1000) % 1_000_000_000
    game_uuid = uuid.uuid4()
    return game_uuid, seed


def get_env_key(name):
    return os.environ.get(name)
