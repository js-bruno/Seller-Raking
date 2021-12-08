import datetime
import os
import operator
from prettytable import PrettyTable
import models
from database import SessionLocal, engine
from sqlalchemy.orm import session 
from utils import print_cordered_sales, create_new_sale, edit_delete_sales, print_all_sales

os.system('cls' if os.name == 'nt' else 'clear')

options = ['Item Count', 'Create New Sale', 'Edit or delete sales']
for index, option in enumerate(options, start=1):
    print(f'{index} - {option}')

selected_option = int(input("Select one of the options:"))
os.system('cls' if os.name == 'nt' else 'clear')

if selected_option == 1:
    item_name_typed = input("Type item Name:")
    print_cordered_sales(item_name_typed)

elif selected_option == 2:
    create_new_sale()

elif selected_option == 3:
    edit_delete_sales()
    

