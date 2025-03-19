import json
import configparser
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models import create_tables, Publisher, Book, Sale, Shop, Stock

config = configparser.ConfigParser()
config.read('settings.ini')
login = config['auth']['login']
password = config['auth']['password']

DSN = f'postgresql://{login}:{password}@localhost:5432/homework_6_db'
engine = sqlalchemy.create_engine(DSN)

create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

with open('fixtures/tests_data.json', 'r') as fd:
    data = json.load(fd)

for record in data:
    model = {
        'publisher': Publisher,
        'shop': Shop,
        'book': Book,
        'stock': Stock,
        'sale': Sale,
    }[record.get('model')]
    session.add(model(id=record.get('pk'), **record.get('fields')))

session.commit()


def get_shops(param):
    selected = session.query(Book.title, Shop.name, Sale.price, Sale.date_sale).select_from(Shop).\
        join(Stock).\
        join(Book).\
        join(Publisher).\
        join(Sale)
    if param.isdigit():
        res = selected.filter(Publisher.id == param).all()
    else:
        res = selected.filter(Publisher.name == param).all()
    for book, shop, cost, date in res:
        print(f"{book: <40} | {shop: <10} | {cost: <8} | {date.strftime('%d-%m-%Y')}")


if __name__ == '__main__':
    pub = input("Введите имя или айди публициста: ")
    get_shops(pub)
