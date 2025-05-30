from database import get_connection
import logging

# Setup basic logging
logging.basicConfig(level=logging.INFO)

def create_table():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Create Matches table with UNIQUE constraint to prevent duplicates
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Matches (
                id SERIAL PRIMARY KEY,
                home_team VARCHAR(255),
                away_team VARCHAR(255),
                match_time TIMESTAMP,
                UNIQUE(home_team, away_team, match_time)
            )
        ''')

        conn.commit()
        logging.info("✅ Matches table created or already exists.")
    except Exception as e:
        logging.error("❌ Error while creating Matches table: %s", e)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
