from datetime import datetime


def to_datetime(str_date: str):
    return datetime.strptime(str_date, '%d.%m.%Y')


def str_to_datetime(str_date: str):
    return datetime.strptime(str_date, '%d.%m.%Y %H:%M:%S')


def get_current_date():
    return datetime.now().date()

def get_current_timestamp(str_date: str):
    return datetime.strptime(str_date, '%Y-%m-%d %H:%M:%S')

def to_datetime_default(str_date: str):
    date_format = "%a, %d %b %Y %H:%M:%S %Z"
    return datetime.strptime(str_date, date_format)

def get_current_hour():
    return datetime.now().hour


if __name__ == '__main__':
    x = '19.07.2022'
    y = '26.07.2022'
    delta = (to_datetime(y) - to_datetime(x)).days
    print()
