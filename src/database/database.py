import psycopg2
from config import Config


class PDataBase:
    def __init__(self):
        self.conn = psycopg2.connect(
            host=Config.DataBase.HOST,
            port=Config.DataBase.PORT,
            database=Config.DataBase.DB,
            user=Config.DataBase.USERNAME,
            password=Config.DataBase.PASSWORD,
        )

    def __del__(self):
        self.conn.close()

    def create_tables(self):
        create_table_query = """ CREATE TABLE IF NOT EXISTS users (
                        ID  SERIAL PRIMARY KEY,
                        name VARCHAR(50) NOT NULL 
                    );"""
        cursor = self.conn.cursor()
        cursor.execute(create_table_query)
        self.conn.commit()
        cursor.close()

    def add_user(self, username):
        add_query = f"""INSERT INTO users (name) VALUES ('{username}')"""
        cursor = self.conn.cursor()
        cursor.execute(add_query)
        self.conn.commit()
        cursor.close()

    def find_user(self, username):
        add_query = f"""SELECT name FROM users WHERE users.name = '{username}'"""
        cursor = self.conn.cursor()
        cursor.execute(add_query)
        name = cursor.fetchone()
        cursor.close()
        return name

    def delete_user(self, username):
        del_query = f"""DELETE FROM users WHERE users.name = '{username}'"""
        cursor = self.conn.cursor()
        cursor.execute(del_query)
        self.conn.commit()
        cursor.close()


db = PDataBase()
