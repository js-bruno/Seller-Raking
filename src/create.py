"""
Creates data to populate the Saler and Saller columns.
"""

from random import randrange, uniform

from sqlalchemy.sql.sqltypes import Float, String
from database import SessionLocal, engine
import models

models.Base.metadata.create_all(bind=engine)


def create_seller(seller_name: String):
    """
    Creates a new row from the Seller column
    """
    new_seller = models.Seller(name=seller_name)
    return new_seller


def create_sale(
    customer_name: String, date_sale: String, item_name: String, item_value: Float
):
    """
    Creates a new row from the Sale column
    """
    sale = models.Sale(
        customer_name=customer_name,
        date_sale=date_sale,
        item_name=item_name,
        item_value=item_value,
    )
    return sale


sellers_names = ["Bruno", "Claudio", "Rodrigo", "Pedro", "Victor"]
customer_names = ["Raissa", "Ubirani", "Gabriela", "Sergio", "Amaro"]
items_names = ["Macarrão", "Feijoada", "Limão", "Batata", "Queijo"]
sellers = []
sales = []

for name in sellers_names:
    sellers.append(create_seller(name))

for seller in sellers:
    for index in range(randrange(1, 5)):
        seller.sales.append(
            create_sale(
                customer_name=customer_names[randrange(4)],
                date_sale=f"{randrange(2001,2020)}/{randrange(1,12)}/{randrange(10,30)}",
                item_name=items_names[randrange(0, 4)],
                item_value=round(uniform(1.5, 24.5), 2),
            )
        )

with SessionLocal() as session:
    for seller in sellers:
        session.add(seller)
        session.add_all(seller.sales)
    session.commit()
    print("Database created successfully")
