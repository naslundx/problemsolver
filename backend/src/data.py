from cachetools.func import ttl_cache
import json
from .database import DB, GAMES_TABLE, QUESTIONS_TABLE, CHATS_TABLE
from .settings import DATA_TTL


def create_game(game_uuid, seed, question_id):
    query = f"""
        INSERT INTO {GAMES_TABLE}
        (game_uuid, seed, question_id)
        VALUES (%s, %s, %s);
    """
    DB.execute(query, params=(str(game_uuid), seed, question_id))


def increment_game_progress(game_uuid, question_id):
    query = f"""
        UPDATE {GAMES_TABLE}
        SET question_id = %s
        WHERE game_uuid = %s;
    """
    DB.execute(query, params=(question_id, str(game_uuid)))


def fetch_game_progress(game_uuid) -> int:
    query = f"""
        SELECT question_id
        FROM {GAMES_TABLE}
        WHERE game_uuid = %s;
    """
    return DB.query(query, single=True, params=(str(game_uuid),)) or 0


@ttl_cache(ttl=DATA_TTL)
def fetch_seed_from_game_uuid(game_uuid) -> int:
    query = f"""
        SELECT seed
        FROM {GAMES_TABLE}
        WHERE game_uuid = %s;
    """
    return DB.query(query, single=True, params=(str(game_uuid),)) or 0


@ttl_cache(ttl=DATA_TTL)
def fetch_question(question_id) -> dict:
    query = f"""
        SELECT content
        FROM {QUESTIONS_TABLE}
        WHERE id = %s; -- AND active = '1';
    """
    content = DB.query(query, single=True, params=(question_id,)) or "{}"
    return json.loads(content)


def fetch_question_count() -> int:
    query = f"""
        SELECT COUNT(*)
        FROM {QUESTIONS_TABLE};
    """

    return DB.query(query, single=True) or 0


def save_chat(game_uuid, chat_index, question_id, question, answer):
    query = f"""
        INSERT INTO {CHATS_TABLE}
        (game_uuid, chat_index, question_id, question, answer)
        VALUES (%s, %s, %s, %s, %s)
    """
    DB.execute(query, params=(game_uuid, chat_index, question_id, question, answer))
