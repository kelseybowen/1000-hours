import sqlite3
from sqlite3 import Error
from HourLog import HourLog
from User import User
from datetime import *


class SQLiteClient:

    def __init__(self, db_file):
        self.conn = None
        try:
            self.conn = sqlite3.connect(db_file)
        except Error as e:
            print(e)

    def create_table(self, create_table_sql):
        try:
            c = self.conn.cursor()
            c.execute(create_table_sql)
        except Error as e:
            print(e)

    def create_users_table(self):

        sql_create_users_table = """ CREATE TABLE IF NOT EXISTS users (
                                            id integer PRIMARY KEY,
                                            username text NOT NULL,
                                            hour_target integer
                                            ); """

        if self.conn is not None:
            self.create_table(sql_create_users_table)
        else:
            print("Error! cannot create the database connection.")

    def create_hours_table(self):

        sql_create_hours_table = """ CREATE TABLE IF NOT EXISTS hours (
                                            id integer PRIMARY KEY,
                                            date text NOT NULL,
                                            user_id text NOT NULL,
                                            hour_count integer,
                                            FOREIGN KEY (user_id) REFERENCES users (id)
                                            ); """

        if self.conn is not None:
            self.create_table(sql_create_hours_table)
        else:
            print("Error! cannot create the database connection.")

    def create_user(self, username, hour_target):

        sql = ''' INSERT INTO users(username,hour_target)
                  VALUES(?,?) '''
        cur = self.conn.cursor()
        cur.execute(sql, (username, hour_target))
        self.conn.commit()
        new_user = User(cur.lastrowid, username, hour_target)
        return new_user

    def get_user_by_id(self, user_id):

        cur = self.conn.cursor()
        cur.execute("SELECT * from users WHERE user_id=?", (user_id,))

        row = cur.fetchone()

        return User(row[0], row[1], row[2])

    def get_user_by_username(self, username):

        cur = self.conn.cursor()
        cur.execute("SELECT * from users WHERE username=?", (username,))

        row = cur.fetchone()

        return User(row[0], row[1], row[2])

    def delete_user(self, user_id):

        cur = self.conn.cursor()
        cur.execute("DELETE FROM users WHERE id=?", (user_id,))
        self.conn.commit()

    def update_user_hour_target(self, user_id, new_target):

        sql = '''UPDATE users SET hour_target=? WHERE id=?'''

        cur = self.conn.cursor()
        cur.execute(sql, (new_target, user_id))
        self.conn.commit()

    def create_hour_log(self, user_id, date, hour_input):

        sql = '''INSERT INTO hours(user_id,date,hour_count) VALUES(?,?,?)'''

        cur = self.conn.cursor()
        cur.execute(sql, (user_id, datetime.strftime(date, "%Y-%m-%d"), hour_input))
        self.conn.commit()
        return cur.lastrowid

    def get_hour_log_id(self, date, user_id):

        sql = '''SELECT id FROM hours WHERE date=? AND user_id=?'''

        cur = self.conn.cursor()
        cur.execute(sql, (date, user_id,))
        rows = cur.fetchall()

        for row in rows:
            print(row)

        return rows if len(rows) > 0 else None

    def get_hour_log(self, hour_log_id):

        sql = '''SELECT * FROM hours WHERE id=?'''

        cur = self.conn.cursor()
        cur.execute(sql, (hour_log_id,))
        row = cur.fetchone()

        log = HourLog(row[0], row[1], row[2], row[3], False)
        return log

    def update_hour_log(self, hour_log_id, hour_count):

        sql = '''UPDATE hours SET hour_count=? WHERE id=?'''

        cur = self.conn.cursor()
        cur.execute(sql, (hour_count, hour_log_id))
        self.conn.commit()

    def delete_hour_log(self, hour_log_id):

        cur = self.conn.cursor()
        cur.execute("DELETE FROM hours WHERE id=?", (hour_log_id,))
        self.conn.commit()

    def get_all_hour_logs_range(self, user_id, start_date, end_date):

        sql = '''SELECT * FROM hours WHERE user_id=? AND date BETWEEN ? AND ? ORDER BY date ASC'''

        cur = self.conn.cursor()
        cur.execute(sql, (user_id, start_date, end_date))
        rows = cur.fetchall()

        hour_log_range_list = []
        for row in rows:
            log = HourLog(row[0], row[1], row[2], row[3], False)
            hour_log_range_list.append(log)

        return hour_log_range_list if len(hour_log_range_list) > 0 else None

