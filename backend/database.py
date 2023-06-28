import json
import psycopg2
import os
from functools import lru_cache
from .helpers import get_ttl_hash
import psycopg2.extras


psycopg2.extras.register_uuid()


DB_CONN = None
DATABASE_URL = os.environ.get("DATABASE_URL", None)
if DATABASE_URL:
    DB_CONN = psycopg2.connect(DATABASE_URL, sslmode="require")

# ---


def _db_exec(query, get_value=False, params=None):
    if not DB_CONN:
        return None

    with (cursor := DB_CONN.cursor()):
        try:
            cursor.execute(query, params)
            DB_CONN.commit()
            if get_value:
                id_of_new_row = cursor.fetchone()[0]
                return id_of_new_row
        except:
            return None


def _db_query(query, single=False, params=None):
    if not DB_CONN:
        return None

    with (cursor := DB_CONN.cursor()):
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
        """
        DROP TABLE IF EXISTS games;
    """
    )
    _db_exec(
        """
        CREATE TABLE games (
            id SERIAL PRIMARY KEY,
            when TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            game_uuid UUID UNIQUE NOT NULL,
            seed INTEGER NOT NULL,
            question_id INTEGER DEFAULT 0
        );
    """
    )
    _db_exec(
        """
        DROP TABLE IF EXISTS questions;
    """
    )
    _db_exec(
        """
        CREATE TABLE questions (
            id INTEGER PRIMARY KEY,
            content text NOT NULL
        );
    """
    )
    _db_exec(
        """
        DROP TABLE IF EXISTS stats;
    """
    )


def upload_questions(filename):
    with open(filename) as f:
        questions = json.loads(f.read())
    _db_exec(
        """
        DELETE FROM questions;
    """
    )
    query = """
        INSERT INTO questions(id, content)
        VALUES
            (%s, %s);
    """
    for question in questions:
        _db_exec(query, params=(question["id"], json.dumps(question)))


# ---


def create_game(game_uuid, seed, question_id):
    query = """
        INSERT INTO games
        (game_uuid, seed, question_id)
        VALUES (%s, %s, %s);
    """
    _db_exec(query, params=(str(game_uuid), seed, question_id))


def increment_game_progress(game_uuid, question_id):
    query = """
        UPDATE games
        SET question_id = question_id + 1
        WHERE game_uuid = %s
        AND question_id = %s;
    """
    _db_exec(query, params=(str(game_uuid), question_id))


def fetch_game_progress(game_uuid):
    query = """
        SELECT question_id
        FROM games
        WHERE game_uuid = %s;
    """
    return _db_query(query, single=True, params=(str(game_uuid),))


@lru_cache()  # TODO use cachetools https://stackoverflow.com/a/54357155
def _fetch_question(question_id, ttl_hash=None):
    del ttl_hash

    query = """
        SELECT content
        FROM questions
        WHERE id = %s; -- AND active = '1';
    """
    content = _db_query(query, single=True, params=(question_id,))
    return json.loads(content)


def fetch_question(question_id):
    return _fetch_question(question_id, ttl_hash=get_ttl_hash())


@lru_cache()
def _fetch_question_count(ttl_hash=None):
    del ttl_hash

    query = """
        SELECT COUNT(*)
        FROM questions;
    """

    return _db_query(query, single=True)


def fetch_question_count():
    return _fetch_question_count(ttl_hash=get_ttl_hash())
