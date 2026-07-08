import sqlite3


class Database:
    def __init__(self, db_name='history.db'):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            height REAL,
            weight REAL,
            bmi REAL,
            category TEXT,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            image_path TEXT
            )
        ''')
        self.connection.commit()

    def add_record(self, height, weight, bmi, category, image_path=''):
        self.cursor.execute('''
            INSERT INTO history (height, weight, bmi, category, image_path)
            VALUES (?, ?, ?, ?, ?)
        ''', (height, weight, bmi, category, image_path))
        self.connection.commit()
        return self.cursor.lastrowid

    def get_all_records(self, limit=50):
        self.cursor.execute('''
            SELECT * FROM history
            ORDER BY date DESC
            LIMIT ?
        ''', (limit,))
        return self.cursor.fetchall()

    def get_record_by_id(self, record_id):
        self.cursor.execute('''
            SELECT * FROM history WHERE id = ?
        ''', (record_id,))
        return self.cursor.fetchone()

    def delete_record(self, record_id):
        self.cursor.execute('''
            DELETE FROM history WHERE id = ?
        ''', (record_id,))
        self.connection.commit()

    def clear_history(self):
        self.cursor.execute('DELETE FROM history')
        self.connection.commit()

    def get_count(self):
        self.cursor.execute('SELECT COUNT(*) FROM history')
        return self.cursor.fetchone()[0]

    def close(self):
        self.connection.close()