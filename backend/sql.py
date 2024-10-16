import sqlite3


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
    token = "RANDOMTOKEN"

    cursor.execute(
        """
        INSERT INTO tokens (uid, username, cid, token)
        VALUES (?, ?, ?, ?)
    """,
        (uid, username, cid, token),
    )

    conn.commit()
    conn.close()

    return token


if __name__ == "__main__":
    create_database()
