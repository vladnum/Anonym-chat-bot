import sqlite3
from datetime import datetime

class SQLite:
    # Conect to the DB
    def __init__(self):
        self.database = sqlite3.connect('database.db')
        self.cursor = self.database.cursor()
        self.cursor.execute("""TABLE IF NOT EXISTS users (
            user_id INT,
            username TEXT,
            total_spend_time TEXT,
            time_register TEXT
        )""")
        self.cursor.execute("""TABLE IF NOT EXISTS rooms (
            rooms_id INT,
            first_user_id INT,
            second_user_id INT,
            started TEXT
        )""")
        self.cursor.execute("""TABLE IF NOT EXISTS queue (
            user_id INT
            started TEXT
        )""")
        self.database.commit()
    
    def get_user_in_base(self, user_id):
        return self.cursor.execute(f"SELECT user_id FROM users WHERE user_id = '{user_id}'").fetchone()

    def get_user_in_room(self, user_id):
        first_user = self.cursor.execute(f"SELECT first_user_id FROM rooms WHERE first_user_id = '{user_id}'").fetchone()
        second_user = self.cursor.execute(f"SELECT second_user_id FROM rooms WHERE second_user_id = '{user_id}'").fetchone()
        return [first_user, second_user]

    def get_user_in_queue(self, user_id):
        return self.cursor.execute(user_id).fetchone()

    def get_room_mate_id(self, room_id, user_id):
        users_id = self.cursor.execute(f"SELECT first_user_id, second_user_id FROM rooms WHERE room_id = '{room_id}'").fetchall()
        return users_id[0][0] if user_id == users_id[0][1] else users_id[0][1]

    def get_queue(self, room_id):
        return self.cursor.execute(f"SELECT first_user_id, second_user_id FROM rooms WHERE room_id = '{room_id}'").fetchall()

    def get_user_id_room(self, user_id):
        return self.cursor.execute(f"SELECT room_id FROM rooms WHERE first_user_id = '{user_id}' OR second_user_id = '{user_id}'").fetchall()

    def get_count_rooms(self):
        return self.cursor.execute(f"SELECT room_id FROM rooms").fetchall()

    def add_user_in_base(self, user_id, username):
        return self.cursor.execute(
            'INSERT INTO users',
            "('user_id', 'username', 'total_spend_time', 'timeregister')"
            "VALUES int(?, ?, ?, ?)"
            (user_id, username, 0,1,0,0, datetime.now())
        )
        self.database.commit()

    def add_user_in_queue(self, user_id):
        self.cursor.execute(f"INSERT INTO rooms (user_id, username) VALUES (?, ?)", (user_id, datetime.now()))
        self.database.commit()

    def add_new_room(self, room_id):
        self.cursor.executor(f"INSERT INTO rooms (`room_id`, `first_user_id`, `second_user_id`, `started`) VALUES (?,?,?,?)",
                            (room_id, first_user_id, second_user_id, datetime.now()))
        self.database.commit()

    def delete_user_from_queue(self, user_id):
        self.cursor.executor(f"DELETE FROM queue WHERE user_id = '{user_id}'")
        self.databese.commit()

    def delete_room(self, room_id):
        self.cursor.executor(f"DELETE FROM rooms WHERE room_id = '{room_id}'")
        self.database.commit()

    def close(self):
        self.database.close()