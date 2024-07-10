from clcrypto import hash_password
from psycopg2 import connect, OperationalError
class users:
    """
    Users support.

    All parameters are optional and have empty values. It is important when the application
    will load objects from the database.

    :param username: username or login
    :param password: user password
    :param salt: cryptography for password
    """
    def __init__(self, username="", password="", salt=""):
        self._id = -1
        self.username = username
        self._hashed_password = hash_password(password, salt)

    @property
    def id(self):
        return self._id

    @property
    def hashed_password(self):
        return self._hashed_password

    def set_password(self, password, salt=""):
        self._hashed_password = hash_password(password, salt)

    @hashed_password.setter
    def hashed_password(self, password):
        self.set_password(password)

    def save_to_db(self, cursor):
        if self._id == -1:
            sql = """INSERT INTO users(username, hashed_password) VALUES(%s, %s) RETURNING id"""
            values = (self.username, self.hashed_password)
            cursor.execute(sql, values)
            self._id = cursor.fetchone()[0]  # przypisanie do atrybutu id wartości z bazy danych stworzonego obiektu
            return True

        else:
            sql = """UPDATE users SET username=%s, hashed_password=%s WHERE id=%s"""
            values = (self.username, self.hashed_password, self.id)
            cursor.execute(sql, values)
            return True

    @staticmethod
    def load_user_by_username(cursor, username):
        sql = "SELECT id, username, hashed_password FROM users WHERE username=%s"
        cursor.execute(sql, (username,))
        data = cursor.fetchone()
        if data:
            id_, username, hashed_password = data
            loaded_user = users(username)
            loaded_user._id = id_
            loaded_user._hashed_password = hashed_password
            return loaded_user

    @staticmethod
    def load_user_by_id(cursor, id_):
        sql = "SELECT id, username, hashed_password FROM users WHERE id=%s"
        cursor.execute(sql, (id_,))  # (id_, ) - cause we need a tuple
        data = cursor.fetchone()
        if data:
            id_, username, hashed_password = data
            loaded_user = users(username)
            loaded_user._id = id_
            loaded_user._hashed_password = hashed_password
            return loaded_user

    @staticmethod
    def load_all_users(cursor):
        sql = "SELECT id, username, hashed_password FROM users"
        users_list = []
        cursor.execute(sql)
        for row in cursor.fetchall():
            id_, username, hashed_password = row
            loaded_user = users()
            loaded_user._id = id_
            loaded_user.username = username
            loaded_user._hashed_password = hashed_password
            users_list.append(loaded_user)
        return users_list

    def delete(self, cursor):
        sql = "DELETE FROM Users WHERE id=%s"
        cursor.execute(sql, (self.id,))
        self._id = -1
        return True

class messages:
    """
    Support for saving and loading messages to/from the database.

    All parameters are optional and have empty values. It is important when the application
    will load objects from the database.

    :param from_id: user id, who is sender
    :param to_id: user id, who is reciever
    :param text: content of the message
    :param creation_date: date the message was created, default = None
    """
    def __init__(self, from_id="", to_id="", text="", creation_date=None):
        self._id = -1
        self.from_id = from_id
        self.to_id = to_id
        self.text = text
        self.creation_date = creation_date

    def __str__(self):
        return f"{self._id}: From: {self.from_id} To: {self.to_id}, Text: {self.text}, Date: {self.creation_date}"

    def __repr__(self):
        return f"{self._id}: From: {self.from_id} To: {self.to_id}, Text: {self.text}, Date: {self.creation_date}"

    @property
    def id(self):
        return self._id

    def save_to_db(self, cursor):
        try:
            if self._id == -1:
                sql = """INSERT INTO messages(from_id, to_id, creation_date, text) VALUES(%s, %s, %s, %s)RETURNING id"""
                values = (self.from_id, self.to_id, self.creation_date, self.text)
                cursor.execute(sql, values)
                self._id = cursor.fetchone()[0]  # or cursor.fetchone()['id']
                return True

            else:
                sql = """UPDATE messages SET from_id=%s, to_id=%s, creation_date=%s, text=%s WHERE id=%s"""
                values = (self.from_id, self.to_id, self.creation_date, self.text)
                cursor.execute(sql, values)
                return True
        except Exception as e:
            print(f'Wystąpił błąd: {e}')
    @staticmethod
    def load_all_messages(cursor):
        try:
            sql = "SELECT id, from_id, to_id, creation_date, text FROM messages"
            messages_list = []
            cursor.execute(sql)
            for row in cursor.fetchall():
                id_, from_id, to_id, creation_date, text = row
                loaded_message = messages(from_id, to_id, text, creation_date)
                loaded_message._id = id_

                messages_list.append(loaded_message)
            return messages_list
        except Exception as e:
            print(f'Wystąpił błąd {e}')

            
if __name__ == "__main__":
    try:
        cnx = connect(user='postgres', password='coderslab', host='127.0.0.1', database='communicator')
        cnx.autocommit = True
        cursor = cnx.cursor()
        user1 = users('Janek', 'motyl123')
        user1.save_to_db(cursor)
        user1_id = user1._id
        assert user1_id != -1
        user1_from_db = user1.load_user_by_id(cursor, user1_id)
        assert user1_from_db.id == user1_id
        print(user1_from_db.id)
        assert user1_from_db.username == 'Janek'
        print(user1_from_db.username)
        assert user1_from_db.hashed_password == hash_password('motyl123', "")
        print(user1_from_db.hashed_password)  # printy przydatne do wizualnego testowania
        #message1 = messages(user1._id, user1_id, 'wiadomość testowa')
        #message1.save_to_db(cursor)
        #message_all = message1.load_all_messages(cursor)
        #print(message_all)

    except OperationalError:
        print('Błąd!')
    finally:
        cursor.close()
        cnx.close()