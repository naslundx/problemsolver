import json
import psycopg2
import os
from functools import lru_cache
from .helpers import get_ttl_hash


DB_CONN = None
DATABASE_URL = os.environ.get('DATABASE_URL', None)
if DATABASE_URL:
    DB_CONN = psycopg2.connect(DATABASE_URL, sslmode='require')

# ---

def _db_exec(query, get_value=False, params=None):
    if not DB_CONN:
        return None
    
    with cursor := DB_CONN.cursor():
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
    
    with cursor := DB_CONN.cursor():
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
    query = '''
        DROP TABLE IF EXISTS games;
        CREATE TABLE IF NOT EXISTS games (
            id SERIAL PRIMARY KEY,
            game_uuid UUID UNIQUE NOT NULL,
            seed INTEGER NOT NULL,
            question_id INTEGER DEFAULT 0
        );
        DROP TABLE IF EXISTS questions;
        CREATE TABLE IF NOT EXISTS questions (
            id SERIAL PRIMARY KEY,
            prompt VARCHAR(1000) NOT NULL,
            openapi_prompt VARCHAR(1000) NOT NULL,
            correct VARCHAR(100) NOT NULL,
            unit VARCHAR(100) NOT NULL,
            image VARCHAR(1000),
            clues TEXT[],
            variables JSON
        );
    '''

def load_questions(filename):
    # TODO change this, just store the entire json as a serialized blob
    with open(filename) as f:
        questions = json.loads(f.read())
    query = '''
        INSERT INTO questions(prompt, openapi_prompt, correct, unit, image, clues, variables)
        VALUES
            (%s, %s, %s, %s, %s, %s, %s);
    '''
    for question in questions:
        prompt = question['prompt']
        openapi_prompt = question['openapi_prompt']
        correct = question['correct']
        unit = question['unit']
        image = question['image']
        clues = []  # TODO
        variables = {}  # TODO
        params = (prompt, openapi_prompt, correct, unit, image, clues, variables)
        _db_exec(query, params=params)

# ---

def create_game(game_uuid, seed, question_id=1):
    query = '''
        INSERT INTO games
        (game_uuid, seed, question_id)
        VALUES (%s, %s, %s);
    '''
    _db_exec(query, params=(game_uuid, seed, question_id))

def update_game_progress(game_uuid, question_id):
    query = '''
        UPDATE games
        SET question_id = %s
        WHERE game_uuid = %s;
    '''
    _db_exec(query, params=(question_id, game_uuid))

def fetch_game_progress(game_uuid):
    query = '''
        SELECT question_id
        FROM games
        WHERE game_uuid = %s;
    '''
    return _db_query(query, single=True, params=(game_uuid,))

@lru_cache()  # or use cachetools https://stackoverflow.com/a/54357155
def _fetch_question(question_id, ttl_hash=None):
    del ttl_hash

    query = '''
        SELECT *
        FROM questions
        WHERE id = %s;
    '''
    return _db_query(query, single=True, params=(question_id, ))

def fetch_question(question_id):
    return _fetch_question(question_id, ttl_hash=get_ttl_hash())

@lru_cache()
def _fetch_question_count(ttl_hash=None):
    del ttl_hash

    query = '''
        SELECT COUNT(*)
        FROM questions;
    '''

    return _db_query(query, single=True)

def fetch_question_count():
    return _fetch_question_count(ttl_hash=get_ttl_hash())
