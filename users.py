import argparse
from psycopg2 import connect, errors, OperationalError
from models import users
from clcrypto import check_password

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--username", help="username")
parser.add_argument("-p", "--password", help="password")
parser.add_argument("-n", "--new_pass", help="new password")
parser.add_argument("-l", "--list", help="list users", action="store_true")
parser.add_argument("-d", "--delete", help="delete user", action="store_true")
parser.add_argument("-e", "--edit", help="edit user", action="store_true")
parser.print_help()
args = parser.parse_args()


def create_new_user():
    """
    Function of creating new users and save to db: communicator in PostgreSQL

    """
    if len(args.password) < 8:
        print('Podane hasło musi zawierać conajmniej 8 znaków!')
        return
    try:
        cnx = connect(user='postgres', password='coderslab', host='127.0.0.1', database='communicator')
        cnx.autocommit = True
        cursor = cnx.cursor()
        user3 = users(args.username, args.password)
        user3.save_to_db(cursor)
        print('Poprawnie dodano nowego użytkownika!')
    except errors.UniqueViolation:
        print('Podany użytkownik już istnieje!')
    except OperationalError:
        print('Błąd połączenia z bazą danych!')
    finally:
        try:
            cursor.close()
        except Exception as e:
            print(f'Wystąpił błąd podczas zamykania kursora: {e}')
        try:
            cnx.close()
        except Exception as e:
            print(f'Wystąpił błąd podczas zamykania połączenia: {e}')


def editing_user_password():
    """
    Function for editing and creating a new user password.

    """
    try:
        cnx = connect(user='postgres', password='coderslab', host='127.0.0.1', database='communicator')
        cnx.autocommit = True
        cursor = cnx.cursor()
        user4 = users()  # no args in class
        """Tworzenie instancji klasy users bez argumentów w funkcji editing_user_password jest celowe i logiczne 
        w kontekście tego, co funkcja ma zrobić. Konstruktor klasy users jest przygotowany na przyjęcie domyślnych 
        wartości, a właściwe dane użytkownika są wczytywane później z bazy danych. Dzięki temu kod jest bardziej 
        elastyczny i łatwiejszy do zarządzania."""
        user4_from_db = user4.load_user_by_username(cursor, args.username)  # calling a function to a variable
        if user4_from_db:  # if True
            print('Użytkownik istnieje!')
            if check_password(args.password, user4_from_db.hashed_password):
                if len(args.new_pass) < 8:
                    print('Podane hasło musi zawierać conajmniej 8 znaków!')

                else:
                    user4_from_db.set_password(args.new_pass)  # setting new password
                    user4_from_db.save_to_db(cursor)  # update database
                    print('Utworzono nowe hasło użytkownika!')

            else:
                print('Podane hasło jest niepoprawne!')
        else:
            print('Użytkownik nie istnieje!')
    except OperationalError:
        print('Błąd połączenia z bazą danych!')
    finally:
        try:
            cursor.close()
        except Exception as e:
            print(f'Wystąpił błąd podczas zamykania kursora: {e}')
        try:
            cnx.close()
        except Exception as e:
            print(f'Wystąpił błąd podczas zamykania połączenia: {e}')


def delete_user():
    """
    Function to remove an existing user from the database: messenger in PostgreSQL.

    """
    try:
        cnx = connect(user='postgres', password='coderslab', host='127.0.0.1', database='communicator')
        cnx.autocommit = True
        cursor = cnx.cursor()
        user5 = users()
        user5_from_db = user5.load_user_by_username(cursor, args.username)  # calling a function to a variable
        if user5_from_db:
            if check_password(args.password, user5_from_db.hashed_password):
                user5_from_db.delete(cursor)
                print('Usunięto użytkownika z bazy danych!')
            else:
                print("Incorrect Password!")
        else:
            return
    except OperationalError:
        print('Błąd połączenia z bazą danych!')
    finally:
        try:
            cursor.close()
        except Exception as e:
            print(f'Wystąpił błąd podczas zamykania kursora: {e}')
        try:
            cnx.close()
        except Exception as e:
            print(f'Wystąpił błąd podczas zamykania połączenia: {e}')

def load_users():
    """
    Function to load all existing users from database: communicator in PostgreSQL.

    """
    try:
        cnx = connect(user='postgres', password='coderslab', host='127.0.0.1', database='communicator')
        cnx.autocommit = True
        cursor = cnx.cursor()
        user6 = users()
        users_list = user6.load_all_users(cursor)
        for user in users_list:
            print(user.id, user.username)
    except OperationalError:
        print('Błąd połączenia z bazą danych!')
    finally:
        try:
            cursor.close()
        except Exception as e:
            print(f'Wystąpił błąd podczas zamykania kursora: {e}')
        try:
            cnx.close()
        except Exception as e:
            print(f'Wystąpił błąd podczas zamykania połączenia: {e}')



if args.username and args.password and not args.new_pass and not args.list and not args.delete and not args.edit:
    create_new_user()
elif args.username and args.password and args.new_pass and not args.list and not args.delete and args.edit:
    editing_user_password()
elif args.username and args.password and not args.new_pass and not args.list and args.delete and not args.edit:
    delete_user()
elif not args.username and not args.password and not args.new_pass and args.list and not args.delete and not args.edit:
    load_users()
else:
    print("Podano niepoprawne argumenty. Sprawdź dostępne opcje.")