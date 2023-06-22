import psycopg2
import os

DB_CONN = None
DB_URI = os.environ.get('DATABASE_URL', None)
if DB_URI:
    DB_CONN = psycopg2.connect(DB_URI, sslmode='require')

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

def create_game(game_uuid, seed, question_id=1):
    query = '''
        INSERT INTO games
        (game_uuid, seed, question_id)
        VALUES (%s, %s, %s);
    '''
    _db_exec(query, (game_uuid, seed, question_id))

def update_game_progress(game_uuid, question_id):
    query = '''
        UPDATE games
        SET question_id = %s
        WHERE game_uuid = %s;
    '''
    _db_exec(query, (question_id, game_uuid))

def get_game_progress(game_uuid):
    query = '''
        SELECT question_id
        FROM games
        WHERE game_uuid = %s;
    '''
    return _db_query(query, params=(game_uuid,))
