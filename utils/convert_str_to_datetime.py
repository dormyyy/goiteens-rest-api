from datetime import datetime

def to_datetime(str_date: str):
    return datetime.strptime(str_date, '%d.%m.%Y %H:%M')



if __name__ == '__main__':
    x = '19.07.2022 18:12'
    print(to_datetime(x))