from database import get_connection

def create_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Matches(
                   id INT AUTO_INCREMENT PRIMARY KEY,
                   home_team VARCHAR(255),
                   away_team VARCHAR(255),
                   match_time DATETIME)
        ''')
    conn.commit()
    cursor.close()
    conn.close()

