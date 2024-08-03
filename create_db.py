import sqlite3
from datetime import datetime



def create_table(conn):
    """
    Create a table in the SQLite database
    """
    try:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS recordings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date DATETIME NOT NULL,
                filename TEXT NOT NULL,
                transcription TEXT NOT NULL,
                summary TEXT NOT NULL
            );
        ''')
        print("Table created successfully")
    except sqlite3.Error as e:
        print(e)


def add_recording_to_db(conn, filename, transcription, summary):
    """
    Add a new recording to the table
    """
    try:
        c = conn.cursor()
        # Automatically uses the current datetime for the date field
        current_datetime = datetime.now()
        c.execute('''
            INSERT INTO recordings (date, filename, transcription, summary)
            VALUES (?, ?, ?, ?);
        ''', (current_datetime, filename, transcription, summary))
        conn.commit()
    except sqlite3.Error as e:
        print(e)


if __name__ == '__main__':

    database = "recordings.db"

    # Connect to the database
    conn = conn = sqlite3.connect(database)

    # Create the tables
    if conn is not None:
        create_table(conn)

        # Example usage: add a new recording
        # add_recording_to_db(conn, "example.wav", "This is a sample transcription of the audio file.", "a summary!")

        # close the connection
        conn.close()
    else:
        print("Error! cannot create the database connection.")
