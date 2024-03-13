import sqlite3
from sqlite3 import Error

from Classes.Hasher import Hasher
from Classes.DatabaseException import DatabaseNotInitialized
from Classes.DatabaseException import DatabaseSystemUserNotFound

"""

The main class for working with a SQL database. 
All requests go through this class.

"""

class Database:

    inited = False

    @classmethod
    def check_init(cls):
        return cls.inited

    @classmethod
    def init(cls):
            conn = sqlite3.connect('basa.db')
            cursor = conn.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users(
                id INTEGER     UNIQUE,
                name TEXT    UNIQUE,
                password TEXT,
                rank INTEGER,
                bal INTEGER,
                status TEXT,
                record TEXT,
                reg_date DATE
                );
                """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS bans(
                name TEXT,
                reason TEXT,
                unban_date DATE,
                ban_date DATE
                );
                """)
            conn.commit()

            cursor.execute("SELECT * FROM bans WHERE unban_date <= datetime(datetime())")
            buf = cursor.fetchall()
            for i in buf:
                cursor.execute(f"SELECT * FROM users WHERE id = '{i[0]}'")
                buf1 = cursor.fetchall()
                if len(buf1) > 0:
                    cursor.execute("""
                                UPDATE users SET status = "ACTIVE"
                                WHERE id = '""" + buf1[0][0] + """'
                                """)
                    cursor.execute("""
                                DELETE FROM bans
                                WHERE id = '""" + buf1[0][0] + """'
                                """)
            cursor.execute("""
                UPDATE users SET rank = 0
                WHERE rank = 1
                """)

            """ Create system user - The system user is needed to manage id and store some information """
            cursor.execute("SELECT * FROM users")
            buf = cursor.fetchall()
            if len(buf) == 0:
                cursor.execute("""INSERT INTO users(id, name, password, rank, bal, status, reg_date) VALUES(0, 'SYSTEMUSER', '0000', 8, 0, 'ACTIVE', datetime(datetime()))""")

            conn.commit()
            cls.inited = True

    @classmethod
    def _new_user(cls, login, password):
        conn = sqlite3.connect('basa.db')
        cursor = conn.cursor()
        if cls.inited:
            if cls._find_with_name(login) == False:
                
                cursor.execute(f"""SELECT * FROM users WHERE name = 'SYSTEMUSER'""")
                buf = cursor.fetchall()
                if len(buf) == 0:
                    raise DatabaseSystemUserNotFound("System user not found!")
                else:
                    cursor.execute(f"""UPDATE users SET id = {buf[0][0] + 1} WHERE name = 'SYSTEMUSER'""")
                    cursor.execute(f"""INSERT INTO users(id, name, password, rank, bal, status, reg_date)
                                VALUES({buf[0][0]}, '{login}', '{Hasher.hash(password)}', 0, 0, 'ACTIVE', datetime(datetime()))""")
                    conn.commit()
                    return True
            else:
                return False
        else:
            raise DatabaseNotInitialized("Database has not been initialized!")

    @classmethod
    def _del_user(cls, login):
        conn = sqlite3.connect('basa.db')
        cursor = conn.cursor()
        if cls.inited:
            cursor.execute("""
                DELETE FROM bans
                WHERE name = '""" + login + """'
                """)
            conn.commit()
            return True
        else:
            raise DatabaseNotInitialized("Database has not been initialized!")

    @classmethod
    def _find_with_name(cls, login):
        conn = sqlite3.connect('basa.db')
        cursor = conn.cursor()
        if cls.inited:
            cursor.execute(f"SELECT * FROM users WHERE name = '{login}'")
            buf = cursor.fetchall()
            if len(buf) > 0:
                return buf
            else:
                return False
        else:
            raise DatabaseNotInitialized("Database has not been initialized!")

    @classmethod
    def _ban_user(cls, login, reason, time):
        conn = sqlite3.connect('basa.db')
        cursor = conn.cursor()
        if cls.inited:
            cursor.execute("""UPDATE users 
                    SET status = 'BANNED'
                    WHERE name = '""" + login + """' """)
            cursor.execute(f"""INSERT INTO bans(name, reason, unban_date, ban_date)
                    VALUES('{login}', '{reason}', datetime(datetime(), '+{time} seconds'), datetime())
                    """)
            conn.commit()
            return True
        else:
            raise DatabaseNotInitialized("Database has not been initialized!")

    @classmethod
    def _unban_user(cls, login):
        conn = sqlite3.connect('basa.db')
        cursor = conn.cursor()
        if cls.inited:
            cursor.execute("""
                        UPDATE users SET status = "ACTIVE"
                        WHERE name = '""" + login + """'
                        """)
            cursor.execute("""
                        DELETE FROM bans
                        WHERE name = '""" + login + """'
                        """)
            conn.commit()
            return True
        else:
            raise DatabaseNotInitialized("Database has not been initialized!")

    @classmethod
    def _set_record(cls, login, record):
        conn = sqlite3.connect('basa.db')
        cursor = conn.cursor()
        if cls.inited:
            cursor.execute("""
                UPDATE users SET record = '""" + record + """'
                WHERE name = '""" + login + """'
                """)
            conn.commit()
            return True
        else:
            raise DatabaseNotInitialized("Database has not been initialized!")

    @classmethod
    def _clear_record(cls, login):
        conn = sqlite3.connect('basa.db')
        cursor = conn.cursor()
        if cls.inited:
            cursor.execute("""
                    UPDATE users SET record = '0'
                    WHERE name = '""" + u[0] + """'
                    """)
            conn.commit()
            return True
        else:
            raise DatabaseNotInitialized("Database has not been initialized!")
    
    @classmethod
    def _find_with_id(cls, id):
        conn = sqlite3.connect('basa.db')
        cursor = conn.cursor()
        if cls.inited:
            cursor.execute(f"SELECT * FROM users WHERE id = {id}")
            return cursor.fetchall()
        else:
            raise DatabaseNotInitialized("Database has not been initialized!")

    @classmethod
    def _check_name_password(cls, login, password):
        conn = sqlite3.connect('basa.db')
        cursor = conn.cursor()
        if cls.inited:
            cursor.execute(f"SELECT * FROM users WHERE name = '{login}' and password = '{Hasher.hash(password)}'")
            buf = cursor.fetchall()
            if len(buf) > 0:
                if buf[0][5] == "BANNED": # User was banned 
                    cursor.execute(f"SELECT * FROM bans WHERE name = '{login}'")
                    buf = cursor.fetchall()[0]
                    return [buf[0], buf[1], buf[2]] # Send name, reason, date
                else:
                    return 1
            else:
                return 0
        else:
            raise DatabaseNotInitialized("Database has not been initialized!")

    @classmethod
    def _set_balance(cls, login, bal):
        conn = sqlite3.connect('basa.db')
        cursor = conn.cursor()
        if cls.inited:
            cursor.execute(f"SELECT * FROM users WHERE name = '{login}'")
            if len(cursor.fetchall()) > 0:
                cursor.execute("""
                UPDATE users SET bal = '""" + bal + """'
                WHERE name = '""" + login + """'
                """)
                conn.commit()
            else:
                return False
        else:
            raise DatabaseNotInitialized("Database has not been initialized!")

    @classmethod
    def _get_balance(cls, login):
        conn = sqlite3.connect('basa.db')
        cursor = conn.cursor()
        if cls.inited:
            cursor.execute(f"SELECT * FROM users WHERE name = '{login}'")
            if len(cursor.fetchall()) > 0:
                return cursor.fetchall()[0]
            else:
                return False
        else:
            raise DatabaseNotInitialized("Database has not been initialized!")

    @classmethod
    def _get_rank(cls, login):
        conn = sqlite3.connect('basa.db')
        cursor = conn.cursor()
        if cls.inited:
            cursor.execute(f"SELECT * FROM users WHERE name = '{login}'")
            buf = cursor.fetchall()
            if len(buf) > 0:
                return buf[0][3]
            else:
                return False
        else:
            raise DatabaseNotInitialized("Database has not been initialized!")

    @classmethod
    def _get_users(cls):
        conn = sqlite3.connect('basa.db')
        cursor = conn.cursor()
        if cls.inited:
            cursor.execute("SELECT * FROM users")
            buf = cursor.fetchall()
            if len(buf) > 0:
                return buf
            else:
                return False
        else:
            raise DatabaseNotInitialized("Database has not been initialized!")

    @classmethod
    def _set_rank(cls, login, new_rank):
        conn = sqlite3.connect('basa.db')
        cursor = conn.cursor()
        if cls.inited:
            cursor.execute(f"SELECT * FROM users WHERE name = '{login}'")
            if len(cursor.fetchall()) > 0 and new_rank < 8:
                cursor.execute(f"""
                UPDATE users SET rank = {new_rank}
                WHERE name = '""" + login + """'
                """)
                conn.commit()
            else:
                return False
        else:
            raise DatabaseNotInitialized("Database has not been initialized!")

    @classmethod
    def _get_banned_users(cls):
        conn = sqlite3.connect('basa.db')
        cursor = conn.cursor()
        if cls.inited:
            cursor.execute("""SELECT * FROM bans""")
            return cursor.fetchall()
        else:
            raise DatabaseNotInitialized("Database has not been initialized!")



            
