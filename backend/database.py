import json
import psycopg2
import os
from functools import lru_cache
from .helpers import get_ttl_hash, get_env_key
import psycopg2.extras


psycopg2.extras.register_uuid()

# ---

DEBUG = "_debug" if "DEBUG" in os.environ else ""
GAMES_TABLE = f"games{DEBUG}"
QUESTIONS_TABLE = f"questions{DEBUG}"
CHATS_TABLE = f"chats{DEBUG}"

DB_CONNECTION = None
DATABASE_URL = get_env_key("DATABASE_URL")


def connect_database():
    global DB_CONNECTION

    if not DATABASE_URL:
        return None
    
    DB_CONNECTION = psycopg2.connect(DATABASE_URL, sslmode="require")

# ---

def _db_exec(query, get_value=False, params=None):
    if not DB_CONNECTION:
        connect_database()

    try:
        with (cursor := DB_CONNECTION.cursor()):
                cursor.execute(query, params)
                DB_CONNECTION.commit()
                if get_value:
                    id_of_new_row = cursor.fetchone()[0]
                    return id_of_new_row

    except psycopg2.OperationalError:
        connect_database()
        return _db_exec(query, get_value, params)


def _db_query(query, single=False, params=None):
    if not DB_CONNECTION:
        return None

    with (cursor := DB_CONNECTION.cursor()):
        try:
            cursor.execute(query, params)
            if single:
                record = cursor.fetchone()[0]
            else:
                record = cursor.fetchall()
            return record
        except:
            return None


# ---


def reset_database():
    _db_exec(
        f"""
        DROP TABLE IF EXISTS {CHATS_TABLE};
    """
    )
    _db_exec(
        f"""
        DROP TABLE IF EXISTS {QUESTIONS_TABLE};
    """
    )
    _db_exec(
        f"""
        DROP TABLE IF EXISTS {GAMES_TABLE};
    """
    )
    _db_exec(
        f"""
        CREATE TABLE {GAMES_TABLE} (
            id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            game_uuid UUID UNIQUE NOT NULL,
            seed INT NOT NULL,
            question_id INT DEFAULT 0
        );
    """
    )
    _db_exec(
        f"""
        CREATE TABLE {QUESTIONS_TABLE} (
            id INT PRIMARY KEY,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            content text NOT NULL
        );
    """
    )
    _db_exec(
        f"""
        CREATE TABLE {CHATS_TABLE} (
            id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
            question_id INT,
            question text,
            answer text,
            CONSTRAINT fk_question_id
                FOREIGN KEY(question_id)
                    REFERENCES {QUESTIONS_TABLE}(id)
        );
    """
    )


def upload_questions(filename="backend/questions.json"):
    with open(filename) as f:
        questions = json.loads(f.read())
    _db_exec(
        f"""
        DELETE FROM {QUESTIONS_TABLE};
    """
    )
    query = f"""
        INSERT INTO {QUESTIONS_TABLE}(id, content)
        VALUES
            (%s, %s);
    """
    for question in questions:
        _db_exec(query, params=(question["id"], json.dumps(question)))


# ---


def create_game(game_uuid, seed, question_id):
    query = f"""
        INSERT INTO {GAMES_TABLE}
        (game_uuid, seed, question_id)
        VALUES (%s, %s, %s);
    """
    _db_exec(query, params=(str(game_uuid), seed, question_id))


def increment_game_progress(game_uuid, question_id):
    query = f"""
        UPDATE {GAMES_TABLE}
        SET question_id = question_id + 1
        WHERE game_uuid = %s
        AND question_id = %s;
    """
    _db_exec(query, params=(str(game_uuid), question_id))


def fetch_game_progress(game_uuid):
    query = f"""
        SELECT question_id
        FROM {GAMES_TABLE}
        WHERE game_uuid = %s;
    """
    return _db_query(query, single=True, params=(str(game_uuid),))


@lru_cache()  # TODO use cachetools https://stackoverflow.com/a/54357155
def _fetch_question(question_id, ttl_hash=None):
    del ttl_hash

    query = f"""
        SELECT content
        FROM {QUESTIONS_TABLE}
        WHERE id = %s; -- AND active = '1';
    """
    content = _db_query(query, single=True, params=(question_id,))
    return json.loads(content)


def fetch_question(question_id):
    return _fetch_question(question_id, ttl_hash=get_ttl_hash())


@lru_cache()
def _fetch_question_count(ttl_hash=None):
    del ttl_hash

    query = f"""
        SELECT COUNT(*)
        FROM {QUESTIONS_TABLE};
    """

    return _db_query(query, single=True)


def fetch_question_count():
    return _fetch_question_count(ttl_hash=get_ttl_hash())


def save_chat(question_id, question, answer):
    query = f"""
        INSERT INTO {CHATS_TABLE}
        (question_id, question, answer)
        VALUES (%s, %s, %s)
    """
    _db_exec(query, params=(question_id, question, answer))
