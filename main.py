from SQLiteClient import SQLiteClient
from Calendar import Calendar


def main():
    database = "/Users/kbowen/PycharmProjects/1000-hours/1000hoursdev.db"

    db = SQLiteClient(database)
    cal = Calendar("kb", database)
    cal.render_json()


if __name__ == '__main__':
    main()
