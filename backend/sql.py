import sqlite3
from uuid import uuid4


def create_database():
    # Connect to the SQLite database (it will be created if it doesn't exist)
    with sqlite3.connect("tokens.db") as conn:

        # Create a cursor object to interact with the database
        cursor = conn.cursor()

        # Create the tokens table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS tokens (
                uid INTEGER PRIMARY KEY NOT NULL,
                username TEXT NOT NULL,
                cid INTEGER NOT NULL,
                token TEXT NOT NULL
            )
            """
        )

        # Commit the changes and close the connection
        conn.commit()

        print("Database and table created successfully.")


# By default create the database if doesn't exist
create_database()


def generate_token(cursor):
    # get all tokens from the database
    tokens = [row[0] for row in cursor.execute("SELECT token FROM tokens")]

    token = str(uuid4())
    while token in tokens:
        token = str(uuid4())
    print("generated token", token)
    return token


def get_token(cursor, uid, username):
    token = cursor.execute(
        """
        SELECT token
        FROM tokens
        WHERE uid = ? AND username = ?
    """,
        (uid, username),
    ).fetchone()

    return token[0] if token else None


def register_user(uid, username, cid):
    with sqlite3.connect("tokens.db") as conn:
        cursor = conn.cursor()

        value = get_token(cursor, uid, username)
        if value:
            return value

        token = generate_token(cursor)

        cursor.execute(
            """
            INSERT INTO tokens (uid, username, cid, token)
            VALUES (?, ?, ?, ?)
        """,
            (uid, username, cid, token),
        )

        conn.commit()

        print(
            f"User registered successfully. uid: {uid}, "
            f"username: {username}, cid: {cid}, token: {token}"
        )

        return token


def get_cid(username, token):
    with sqlite3.connect("tokens.db") as conn:
        cursor = conn.cursor()

        cid = cursor.execute(
            """
            SELECT cid
            FROM tokens
            WHERE username = ? AND token = ?
        """,
            (username, token),
        ).fetchone()

        return cid[0] if cid else None
