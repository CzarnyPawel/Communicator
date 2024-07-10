from psycopg2 import connect, errors

def create_db():
    """
    A function that creates a new database

    """
    sql = """CREATE DATABASE communicator;"""
    try:
        cnx = connect(user='postgres', password='coderslab', host='127.0.0.1')
        cnx.autocommit = True
        cursor = cnx.cursor()
        cursor.execute(sql)
        print("Baza danych została pomyślnie utworzona!")
    except errors.DuplicateDatabase:
        print('Wskazana baza danych już istnieje!')
    finally:
        cursor.close()
        cnx.close()


#db_name = "users"


def create_table_users():
    """
    A function that creates a new table called: users.

    """
    sql1 = """CREATE TABLE users 
    (
    id serial PRIMARY KEY,
    username varchar(255),
    hashed_password varchar(80)
    );"""
    try:
        cnx = connect(user='postgres', password='coderslab', host='127.0.0.1', database='communicator')
        cnx.autocommit = True
        cursor = cnx.cursor()
        cursor.execute(sql1)
        print('Poprawnie dodano tabelę!')
    except errors.DuplicateTable:
        print("Wskazana tabela już istnieje!")
    finally:
        cursor.close()
        cnx.close()

def create_table_messages():
    """
    A function that creates a new table called: messages.
     
    """
    sql2 = """CREATE TABLE messages
    (
    id serial PRIMARY KEY,
    from_id int,
    to_id int,
    creation_date timestamp default current_timestamp,
    text varchar(255),
    FOREIGN KEY (from_id) REFERENCES users(id),
    FOREIGN KEY (to_id) REFERENCES users(id)
    )"""
    try:
        cnx = connect(user='postgres', password='coderslab', host='127.0.0.1', database='communicator')
        cnx.autocommit = True
        cursor = cnx.cursor()
        cursor.execute(sql2)
        print('Poprawnie dodano tabelę!')
    except errors.Duplicate:
        print('Wskazana tabela już istnieje!')
    finally:
        cursor.close()
        cnx.close()

if __name__ == "__main__":
    create_db()
    create_table_users()
    create_table_messages()