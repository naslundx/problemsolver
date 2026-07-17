import json
import psycopg2
from typing import Any
import psycopg2.extensions
import psycopg2.extras
from .helpers import get_env_key
from .settings import TABLE_SUFFIX


psycopg2.extras.register_uuid()  # type: ignore


class Database:
    def __init__(self) -> None:
        self.connection: psycopg2.extensions.connection | None = None
        self.connect_database()

    def connect_database(self) -> None:
        if not DATABASE_URL:
            return

        self.connection = psycopg2.connect(DATABASE_URL)  # , sslmode="require")

    def execute(
        self, query: str, get_value: bool = False, params: tuple[Any, ...] | None = None
    ) -> int | None:
        if not self.connection:
            self.connect_database()

        try:
            assert self.connection is not None
            with (cursor := self.connection.cursor()):
                cursor.execute(query, params)
                self.connection.commit()
                if get_value:
                    id_of_new_row = cursor.fetchone()
                    if id_of_new_row:
                        return int(id_of_new_row[0])

        except psycopg2.OperationalError:
            self.connect_database()
            return self.execute(query, get_value, params)

        return None

    def query(
        self, query: str, single: bool = False, params: tuple[Any, ...] | None = None
    ) -> Any:
        if not self.connection:
            self.connect_database()

        assert self.connection is not None
        with (cursor := self.connection.cursor()):
            cursor.execute(query, params)
            if single:
                record = cursor.fetchone()
                return record[0] if record else None

            res = cursor.fetchall()
            return res


GAMES_TABLE = f"games{TABLE_SUFFIX}"
QUESTIONS_TABLE = f"questions{TABLE_SUFFIX}"
CHATS_TABLE = f"chats{TABLE_SUFFIX}"
DATABASE_URL = get_env_key("DATABASE_URL")
DB = Database()


def reset_database() -> None:
    DB.execute(
        f"""
        DROP TABLE IF EXISTS {CHATS_TABLE};
    """
    )
    DB.execute(
        f"""
        DROP TABLE IF EXISTS {QUESTIONS_TABLE};
    """
    )
    DB.execute(
        f"""
        DROP TABLE IF EXISTS {GAMES_TABLE};
    """
    )
    DB.execute(
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
    DB.execute(
        f"""
        CREATE TABLE {QUESTIONS_TABLE} (
            id INT PRIMARY KEY,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            content text NOT NULL
        );
    """
    )
    DB.execute(
        f"""
        CREATE TABLE {CHATS_TABLE} (
            id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
            game_uuid UUID NOT NULL,
            chat_index INT NOT NULL,
            question_id INT NOT NULL,
            question text,
            answer text,
            CONSTRAINT fk_question_id
                FOREIGN KEY(question_id)
                    REFERENCES {QUESTIONS_TABLE}(id)
        );
    """
    )
    print("Done.")


def upload_questions(filename: str = "questions.json") -> None:
    with open(filename, encoding="utf-8") as f:
        questions = json.loads(f.read())

    DB.execute(
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
        DB.execute(query, params=(question["id"], json.dumps(question)))
    print("Done.")
