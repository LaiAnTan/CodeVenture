import sqlite3

class AchievementSystem:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS achievements (
                achievement_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE,
                description TEXT,
                criteria INTEGER
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_achievements (
                user_id INTEGER,
                achievement_id INTEGER,
                FOREIGN KEY (user_id) REFERENCES users (user_id),
                FOREIGN KEY (achievement_id) REFERENCES achievements (achievement_id),
                PRIMARY KEY (user_id, achievement_id)
            )
        ''')
        self.conn.commit()

    def add_user(self, username):
        cursor = self.conn.cursor()
        cursor.execute('INSERT INTO users (username) VALUES (?)', (username,))
        self.conn.commit()

    def add_achievement(self, name, description, criteria):
        cursor = self.conn.cursor()
        cursor.execute('INSERT INTO achievements (name, description, criteria) VALUES (?, ?, ?)', (name, description, criteria))
        self.conn.commit()

    def earn_achievement(self, username, achievement_name):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO user_achievements (user_id, achievement_id)
            SELECT users.user_id, achievements.achievement_id
            FROM users, achievements
            WHERE users.username = ? AND achievements.name = ?
        ''', (username, achievement_name))
        self.conn.commit()

    def check_achievements(self, username):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT achievements.name
            FROM achievements
            WHERE achievements.achievement_id NOT IN (
                SELECT achievement_id
                FROM user_achievements
                WHERE user_id = (
                    SELECT user_id
                    FROM users
                    WHERE username = ?
                )
            )
            AND achievements.criteria <= (
                SELECT COUNT(*)
                FROM user_achievements
                WHERE user_id = (
                    SELECT user_id
                    FROM users
                    WHERE username = ?
                )
            )
        ''', (username, username))
        return cursor.fetchall()

if __name__ == "__main__":
    achievement_system = AchievementSystem("achievements.db")

    # Adding users and achievements
    achievement_system.add_user("user1")
    achievement_system.add_achievement("Bronze Badge", "Complete 5 learning modules", 5)
    achievement_system.add_achievement("Silver Badge", "Complete 10 learning modules", 10)

    # Simulate user earning achievements
    achievement_system.earn_achievement("user1", "Bronze Badge")

    # Check for available achievements
    available_achievements = achievement_system.check_achievements("user1")
    print("Available Achievements for user1:", [achievement[0] for achievement in available_achievements])