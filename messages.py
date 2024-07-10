import argparse
from models import messages, users
from psycopg2 import connect, OperationalError
from clcrypto import check_password


parser = argparse.ArgumentParser()
parser.add_argument("-u", "--username", help="username")
parser.add_argument("-p", "--password", help="password")
parser.add_argument("-t", "--to", help="recipient")
parser.add_argument("-s", "--send", help="message")
parser.add_argument("-l", "--list", help="list of messages", action="store_true")

#parser.print_help()
args = parser.parse_args()

def list_of_messages():
    """
    A function that loads all messages from the database for an existing user.

    """
    try:
        cnx = connect(user='postgres', password='coderslab', host='127.0.0.1', database='communicator')
        cnx.autocommit = True
        cursor = cnx.cursor()
        user = users()
        message = messages()
        messages_to_user = message.load_all_messages(cursor)
        user_from_db = user.load_user_by_username(cursor, args.username)
        if user_from_db:
            print('Użytkownik istnieje!')
            if check_password(args.password, user_from_db.hashed_password):
                for one_message in messages_to_user:
                    if user_from_db.id == one_message.to_id: # comparsion of two values
                        print(one_message.to_id, one_message.creation_date, one_message.text)
            else:
                print("Niepoprawne hasło!")
        else:
            print('Brak użytkownika w bazie danych!')
    except OperationalError as e:
        print(f'Wystąpił błąd {e}')
    finally:
        try:
            cursor.close()
        except Exception as e:
            print(f'Wystąpił błąd podczas zamykania kursora: {e}')
        try:
            cnx.close()
        except Exception as e:
            print(f'Wystąpił błąd podczas zamykania połączenia: {e}')

def send_message():
    """
    A function that sends a message from the sender to the recipient.

    """
    try:
        cnx = connect(user='postgres', password='coderslab', host='127.0.0.1', database='communicator')
        cnx.autocommit = True
        cursor = cnx.cursor()
        sender = users()
        recipient = users()
        sender_from_db = sender.load_user_by_username(cursor, args.username)
        recipient_from_db = recipient.load_user_by_username(cursor, args.to)
        message1 = messages(sender_from_db.id, recipient_from_db.id, args.send)
        if sender_from_db:
            print('Użytkownik istnieje!')
            if check_password(args.password, sender_from_db.hashed_password):
                if recipient_from_db:
                    message1.save_to_db(cursor)
                    print('Poprawnie dodano wiadomość do bazy danych!')
                else:
                    print('Wskazany odbiorca nie istnieje w bazie danych!')
            else:
                print('Podane hasło jest nieprawidłowe!')
        else:
            print('Brak użytkownika w bazie danych!')
    except OperationalError as e:
        print(f'Wystąpił błąd {e}')
    finally:
        try:
            cursor.close()
        except Exception as e:
            print(f'Wystąpił błąd podczas zamykania kursora: {e}')
        try:
            cnx.close()
        except Exception as e:
            print(f'Wystąpił błąd podczas zamykania połączenia: {e}')



if args.username and args.password and not args.to and args.list and not args.send:
    list_of_messages()
elif args.username and args.password and args.to and not args.list and args.send:
    send_message()
else:
    print("Podano niepoprawne argumenty. Sprawdź dostępne opcje.")