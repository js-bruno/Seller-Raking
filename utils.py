"""
Utilities to help display logs on the terminal
"""
import os
from prettytable import PrettyTable
import models
from database import SessionLocal

db_sellers = SessionLocal().query(models.Seller).all()


def print_all_sales():
    """
    displays in the terminal a list of all registered sellers
    ranked from highest to lowest sold value
    """
    os.system("cls")
    sales_tables = PrettyTable(
        [
            "Id",
            "Seller Name",
            "Customer Name",
            "Date of Sale",
            "Item Name",
            "Item Value",
        ]
    )

    db_sales_sellers = (
        SessionLocal()
        .query(models.Sale, models.Seller)
        .filter(models.Sale.seller_id == models.Seller.id)
        .all()
    )
    for index, sale_seller in enumerate(db_sales_sellers):
        sales_tables.add_row(
            [
                sale_seller[0].id,
                sale_seller[1].name,
                sale_seller[0].customer_name,
                sale_seller[0].date_sale,
                sale_seller[0].item_name,
                sale_seller[0].item_value,
            ]
        )
    sales_tables.sortby = "Item Value"
    sales_tables.reversesort = True
    print(sales_tables)


def print_cordered_sales(item_name: str):
    """
    Shows on the screen a list of the quantity 
    that each seller has sold for that sales item
    """
    os.system('cls' if os.name == 'nt' else 'clear')
    quantity_table = PrettyTable(
        [
            "Seller Name",
            "Item Name",
            "Quantity",
        ]
    )
    order_sales = []
    for seller in db_sellers:
        item_count = 0
        for index, sale in enumerate(seller.sales):
            if seller.sales[index].item_name == item_name:
                item_count += 1

        order_sales.append({"seller": seller.name, "item_count": item_count})

    sorted_sales = sorted(order_sales, key=lambda x: x["item_count"], reverse=True)

    for sorted_sale in sorted_sales:
        quantity_table.add_row([sorted_sale['seller'], item_name, sorted_sale['item_count']])
    print(quantity_table)

def create_new_sale():
    """
    Creates new sale
    """
    sellers = SessionLocal().query(models.Seller).all()

    for count, seller in enumerate(sellers):
        print(f"{count+1} - {seller.name}")

    seller_choice_number = int(
        input("Enter the number corresponding to your seller registration:")
    )
    os.system('cls' if os.name == 'nt' else 'clear')
    seller_selected = sellers[seller_choice_number - 1]

    customer_name_typed = input("Enter the name of the customer serviced:")
    os.system('cls' if os.name == 'nt' else 'clear')
    date_sale_typed = input("Enter the date(YYYY/MM/DD) the sale took place:")
    os.system('cls' if os.name == 'nt' else 'clear')
    item_name_typed = input("Enter the name of the sales item:")
    os.system('cls' if os.name == 'nt' else 'clear')
    item_value_typed = input("Enter the value of the sales item:")

    new_sale = models.Sale(
        customer_name=customer_name_typed,
        date_sale=date_sale_typed,
        item_name=item_name_typed,
        item_value=item_value_typed,
    )

    with SessionLocal() as session:
        seller = (
            session.query(models.Seller)
            .filter(models.Seller.id == seller_selected.id)
            .first()
        )
        seller.sales.append(new_sale)
        session.add(new_sale)
        session.commit()


def edit_delete_sales():
    """
    Edit or delete sales data persisted in the database
    """
    sale_id = int(input("Enter Sale Id to Edit or Remove it:"))
    os.system('cls' if os.name == 'nt' else 'clear')
    sale_attrs = [
        "Seller Name",
        "Customer Name",
        "Date of Sale",
        "Item Name",
        "Item Value",
    ]
    with SessionLocal() as session:
        db_sale = session.query(models.Sale).filter(models.Sale.id == sale_id).first()
        db_seller = (
            session.query(models.Seller)
            .filter(models.Seller.id == db_sale.seller_id)
            .first()
        )
        sales_tables = PrettyTable(
            [
                "Id",
                "Seller Name",
                "Customer Name",
                "Date of Sale",
                "Item Name",
                "Item Value",
            ]
        )
        sales_tables.add_row(
            [
                db_sale.id,
                db_seller.name,
                db_sale.customer_name,
                db_sale.date_sale,
                db_sale.item_name,
                db_sale.item_value,
            ]
        )

        print(sales_tables)

        for index, sale_attr in enumerate(sale_attrs):
            print(f"{index+1} - {sale_attr}")
        print(f"{index+2} - DELETE IT")

        selected_option = int(input("Select one of the options to Modify:"))
        os.system('cls' if os.name == 'nt' else 'clear')
        if selected_option == 1:
            sellers = session.query(models.Seller).all()
            for count, seller in enumerate(sellers):
                print(f"{count+1} - {seller.name}")
            print(db_seller.name)
            new_value = int(
                input(f"Enter the new value for {sale_attrs[selected_option-1]}:")
            )
            db_seller.sales.remove(db_sale)
            sellers[new_value - 1].sales.append(db_sale)
            session.commit()
            sales_tables.del_row(0)
            sales_tables.add_row([
                db_sale.id,
                sellers[new_value - 1].name,
                db_sale.customer_name,
                db_sale.date_sale,
                db_sale.item_name,
                db_sale.item_value,
            ])
            os.system('cls' if os.name == 'nt' else 'clear')
            print(sales_tables)
        else:
            new_value = input(
                f"Enter the new value for {sale_attrs[selected_option-1]}:"
            )

        if selected_option == 2:
            db_sale.customer_name = new_value
        elif selected_option == 3:
            db_sale.date_sale = new_value
        elif selected_option == 4:
            db_sale.item_name = new_value
        elif selected_option == 5:
            db_sale.value = new_value
        elif selected_option == 6:
            print("REMOVE")

        session.commit()
