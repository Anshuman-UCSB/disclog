import sqlite3
from uuid import uuid4


def generate_token(cursor):
    # get all tokens from the database
    tokens = cursor.execute("SELECT token FROM tokens")

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


def create_database():
    # Connect to the SQLite database (it will be created if it doesn't exist)
    conn = sqlite3.connect("tokens.db")

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
    conn.close()

    print("Database and table created successfully.")


def register_user(uid, username, cid):
    conn = sqlite3.connect("tokens.db")
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
    conn.close()
    print(
        f"User registered successfully. uid: {uid}, "
        f"username: {username}, cid: {cid}, token: {token}"
    )

    return token


create_database()
