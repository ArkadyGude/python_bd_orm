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

# pub = input()
pub = 'O’Reilly'

selected = session.query(Book.title, Shop.name, Sale.price, Sale.date_sale).join(Publisher).join(Stock).join(Shop).join(Sale).filter(Publisher.name.like(pub))
k = [[s[0]] + [s[1]] + [str(s[2])] + [str(s[3])] for s in selected.all()]

for i in k:
    print(*i, sep='\t|\t ')
