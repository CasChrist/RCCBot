import sqlite3

class BotDB:

    def __init__(self, db_file):
        """Инициализация соединения с БД"""
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()

    def show_tables(self):
        self.cursor.execute("SELECT name FROM sqlite_schema WHERE type ='table' AND name NOT LIKE 'sqlite_%';")
        results = self.cursor.fetchall()
        tables = "There are {} table(s) in the database:\n".format(len(results))
        for result in range(len(results)):
            tables += str(result+1) + " " + results[result][0] + "\n"
        return tables

    def user_exists(self, user_id: int):
        """
        Check whether user exists in DB
        :param user_id: Telegram user ID
        """
        self.cursor.execute("SELECT UserID FROM Users WHERE TelegramID = ?;", (user_id,))
        result = self.cursor.fetchone()
        return False if result is None else True
    
    def get_user_id(self, user_id: int):
        """Получает id юзера в базе по его user_id в телеграме"""
        result = self.cursor.execute("SELECT UserID FROM Users WHERE TelegramID = ?;", (user_id,))
        return result.fetchone()
    
    def add_user(self, user_id: int):
        """Добавляет юзера в БД"""
        self.cursor.execute("INSERT INTO Users (TelegramID) VALUES (?);", (user_id,))
        self.cursor.execute("INSERT INTO Preferences (UserID, Videos, Lives) VALUES (?, ?, ?);", (self.get_user_id(user_id)[0], True, True))
        return self.conn.commit()
    
    def update_videos_preference(self, user_id: int, nvideos: bool):
        """Обновляет запись о подключенных уведомлениях на видео"""
        self.cursor.execute("UPDATE Preferences SET Videos = ? WHERE UserID = ?;", (nvideos, self.get_user_id(user_id)[0]))
        return self.conn.commit()
    
    def update_livestreams_preference(self, user_id: int, nlivestreams: bool):
        """Обновляет запись о подключенных уведомлениях на прямые трансляции"""
        self.cursor.execute("UPDATE Preferences SET Lives = ? WHERE UserID = ?;", (nlivestreams, self.get_user_id(user_id)[0]))
        return self.conn.commit()
    
    def get_preferences(self, user_id: int):
        """Получает информацию о подключенных уведомлениях"""
        result = self.cursor.execute("SELECT Preferences.Videos, Preferences.Lives FROM Preferences WHERE Preferences.UserID = ?;", (self.get_user_id(user_id)[0],))
        listed = result.fetchall()
        return [True if value == 1 else False for value in listed[0]]
    
    def delete_all_users(self):
        """Удаляет всех пользователей из БД"""
        self.cursor.execute("DELETE FROM Users;")
        self.cursor.execute("DELETE FROM Preferences;")
        return self.conn.commit()
    
    def close(self):
        """Закрывает соединение с БД"""
        self.conn.close()