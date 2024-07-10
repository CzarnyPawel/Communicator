# Communicator

Napisz w tym celu skrypt pythona: create_db.py, w którym:

    Utworzysz bazę danych. Jeśli baza już istnieje, skrypt ma poinformować o tym użytkownika, nie przerywając swojego działania (Podpowiedź: możesz przechwycić błąd: DuplicateDatabase).
    Stworzysz tabelę trzymającą dane użytkownika (users). Powinna posiadać następujące kolumny:
        id – klucz główny (najlepiej typu serial),
        username – ciąg znaków (varchar(255)),
        hashed_password – ciąg znaków (varchar(80)). Jeżeli istnieje już taka tabela, skrypt powinien poinformować o tym użytkownika, nie przerywając swojego działania (Podpowiedź: możesz przechwycić błąd: DuplicateTable).
    Stworzysz tabelę przechowującą komunikaty (messages). Powinna posiadać następujące kolumny:
        id – klucz główny (najlepiej typu serial),
        from_id – klucz obcy do tabeli users,
        to_id – klucz obcy do tabeli users,
        creation_date – timestamp, dodawany automatycznie,
        text – ciąg znaków (varchar(255)). Jeżeli istnieje już taka tabela, skrypt powinien poinformować o tym użytkownika, nie przerywając swojego działania (Podpowiedź: możesz przechwycić błąd: DuplicateTable).

Pamiętaj o zamknięciu połączenia. Powinieneś też obsłużyć ewentualne błędy połączenia (OperationalError).
Warsztat – Obiektowa obsługa bazy danych

Mamy już stworzoną naszą bazy danych. Pola na stworzenie biblioteki odwzorowującej nasze tabele w postaci obiektów. Utwórz teraz osobny moduł (np. models.py). W nim umieść kod z klasami, obsługującymi poszczególne tabele.
Klasa użytkownika

    Stwórz klasę, obsługującą użytkownika. Powinna ona posiadać następujące atrybuty:
        _id – ustawione podczas tworzenia na -1,
        usename – nazwa użytkownika,
        _hashed_password – zahaszowane hasło użytkownika.
    Udostępnij _id i _hashed_password do odczytu na zewnątrz.
    Dodaj metodę, która pozwoli, na ustawienie nowego hasła (Podpowiedź: możesz użyć settera).
    Dodaj metody do obsługi bazy: save_to_db – zapis do bazy danych lub aktualizacja obiektu w bazie, load_user_by_username – wczytanie użytkownika z bazy danych na podstawie jego nazwy, load_user_by_id – wczytanie użytkownika z bazy danych na podstawie jego id, load_all_users – wczytanie wszystkich użytkowników z bazy danych, delete – usunięcie użytkownika z bazy i nastawienie jego _id na -1.

Podpowiedzi:

    Wszystkie powyższe metody, powinny przyjmować kursor do obsługi bazy danych.
    Możesz wykorzystać kod, który omówiliśmy w artykule poświęconym wzorcowi projektowemu Active Record. Wystarczy, że dodasz do niego metodę, wczytującą użytkownika z bazy na podstawie jego imienia.

Klasa wiadomości

    Utwórz teraz klasę, która będzie obsługiwała nasze wiadomości. Powinna ona posiadać następujące atrybuty:
        _id – ustawione podczas tworzenia na -1,
        from_id – id nadawcy, ustawiane podczas tworzenia obiektu,
        to_id – id odbiorcy, ustawiane podczas tworzenia obiektu,
        text – tekst do przesłania,
        creation_data – data utworzenia wiadomości. Podczas tworzenia przypisz do niej None. Ustawisz ją w momencie zapisu do bazy danych.
    Udostępnij _id na zewnątrz.
    Dodaj metody do obsługi bazy:
        save_to_db – zapis do bazy danych lub aktualizacja obiektu w bazie,
        load_all_messages – wczytanie wszystkich wiadomości.

Podpowiedzi:

    Usuwanie wiadomości, nie będzie nam potrzebne.
    Metody, będą bardzo podobne do tych z klasy użytkownika. Wystarczy, że lekko je zmodyfikujesz.

Pamiętaj, żeby przetestować, czy biblioteka działa. Możesz wykorzystać scenariusze testowe, opisane w artykule omawiającym Active Record.
Warsztat – Aplikacja do obsługi użytkowników

Utwórzmy teraz aplikację, obsługującą naszych użytkowników. Będzie to aplikacja konsolowa, przyjmująca argumenty wprowadzone przez użytkownika. Wykorzystaj do tego bibliotekę argparse. Aplikacja powinna obsługiwać następujące parametry: * -u, --username – nazwa użytkownika, * -p, --password – hasło użytkownika, * -n, --new_pass – nowe hasło, * -l, --list – listowanie użytkowników, * -d, --delete – usuwanie użytkownika, * -e, --edit – edycja użytkownika.

Aplikacja powinna obsługiwać scenariusze opisane poniżej. Najprościej będzie, przygotować osobną funkcję na każdy, ze scenariuszy. W głównym kodzie programu wystarczy wtedy sprawdzić parametry instrukcję if – elif, a następnie wywołać odpowiednie funkcje.
Tworzenie użytkownika

Jeśli podczas wywołania aplikacji, użytkownik poda tylko parametry: username i password:

    jeśli użytkownik o podanej nazwie istnieje – zgłaszamy błąd (Podpowiedź: możesz przechwycić błąd: UniqueViolation),
    jeśli nie ma takiego użytkownika:
        jeśli hasło ma co najmniej 8 znaków, należy go utworzyć, korzystając z podanych danych (pamiętaj, o zapisaniu obiektu do bazy danych),
        jeśli hasło jest za krótkie, należy wyświetlić odpowiedni komunikat.

Edycja hasła użytkownika

Jeśli podczas wywołania aplikacji, użytkownik poda parametry:

    username,
    password,
    edit,
    new_pass, powinniśmy:
    sprawdzić, czy użytkownik istnieje
    sprawdzić, czy hasło jest poprawne:
        jeśli tak, sprawdzamy, czy nowe hasło (new_pass) ma wymaganą długość:
            jeśli jest krótsze niż 8 znaków, zgłaszamy to odpowiednim komunikatem,
            jeśli jest wystarczającej długości, ustawiamy nowe hasło,
        jeśli hasło jest niepoprawne, zgłaszamy to odpowiednim komunikatem.

    Podpowiedź: Do sprawdzenia hasła, możesz wykorzystać funkcję check_password z biblioteki clcrypto.

Usuwanie użytkownika

Jeśli podczas wywołania aplikacji, użytkownik poda parametry:

    username,
    password,
    delete, należy:
    sprawdzić poprawność hasła,
        jeśli jest poprawne – usunąć użytkownika z bazy danych,
        jeśli jest niepoprawne – poinformować o tym użytkownika odpowiednim komunikatem np. "Incorrect Password!.

Listowanie użytkowników:

Jeśli podczas wywołania aplikacji, użytkownik poda parametr -l (--list), należy wypisać listę wszystkich użytkowników.
Pomoc

Jeśli użytkownik poda inny zestaw parametrów, należy wyświetlić mu panel pomocy. Można to zrobić, wywołując: metodę print_help z obiektu parsera.
Przykład:

import argparse

parser = argparse.ArgumentParser()
parser.print_help()

Warsztat – Aplikacja do obsługi wiadomości

Stwórzmy teraz naszą główną aplikację. Będzie to program konsolowy pozwalający wysyłać i odczytywać wiadomości. Aplikacja powinna przyjmować od użytkownika następujące argumenty:

    -u, --username – nazwa użytkownika,
    -p, --password – hasło użytkownika,
    -t, --to – nazwa użytkownika, do którego ma zostać wysłana wiadomość,
    -s, --send – treść wiadomości,
    -l, --list – żądanie wylistowania wszystkich komunikatów użytkownika (flaga).

Do parsowania argumentów użyj biblioteki argparse.

Aplikacja powinna obsługiwać scenariusze opisane poniżej. Najprościej będzie, przygotować osobną funkcję na każdy, ze scenariuszy. W głównym kodzie programu wystarczy wtedy sprawdzić parametry instrukcję if – elif, a następnie wywołać odpowiednie funkcje.
Listowanie wiadomości

Jeśli podczas wywołania aplikacji, użytkownik poda parametry: username i password oraz ustawi flagę -l:

    sprawdź, czy użytkownik istnieje, jeśli nie wyświetl odpowiedni komunikat,
    sprawdź, czy hasło jest poprawne:
        jeśli nie, wyświetl odpowiedni komunikat,
        jeśli tak, wypisz wszystkie wiadomości wysłane do tego użytkownika.

Każda z wiadomości powinna zawierać:

    adresata,
    datę wysłania wiadomości,
    treść wiadomości.

Wysłanie wiadomości

Jeśli podczas wywołania aplikacji, użytkownik poda parametry: username i password oraz dodatkowo ustawi parametr -t (--to) i -s (--send):

    sprawdź, czy użytkownik istnieje, jeśli nie wyświetl odpowiedni komunikat,
    sprawdź, czy hasło jest poprawne:
        jeśli nie, wyświetl odpowiedni komunikat,
        jeśli tak:
            sprawdź, czy adresat wiadomości istnieje (--to), jeśli nie, poinformuj o tym użytkownika,
            sprawdź, czy wiadomość jest krótsza, niż 255 znaków:
                jeśli nie, wyświetl odpowiedni komunikat,
                jeśli tak, utwórz wiadomość i zapisz ją do bazy danych.

Pomoc

Jeśli użytkownik poda inny zestaw parametrów, należy wyświetlić mu panel pomocy. Można to zrobić, wywołując: metodę print_help z obiektu parsera.
