# pathlib is a library that provides an object-oriented interface to the filesystem
# it is a more modern and pythonic way to work with files and directories
# docs: https://docs.python.org/3/library/pathlib.html

from pathlib import Path
from database import get_connection, insert_customer_query, insert_order_query, insert_product_query
import csv 
import re 
from dateutil.parser import parse


country_map = {
    "UNITEDSTATES": "USA",
    "US": "USA",
    "USA": "USA",
    "UNITED": "USA",
}

state_map = {
    "ALABAMA": "AL",
    "ALASKA": "AK",
    "ARIZONA": "AZ",
    "ARKANSAS": "AR",
    "CALIFORNIA": "CA",
    "COLORADO": "CO",
    "CONNECTICUT": "CT",
    "DELAWARE": "DE",
    "FLORIDA": "FL",
    "GEORGIA": "GA",
    "HAWAII": "HI",
    "IDAHO": "ID",
    "ILLINOIS": "IL",
    "INDIANA": "IN",
    "IOWA": "IA",
    "KANSAS": "KS",
    "KENTUCKY": "KY",
    "LOUISIANA": "LA",
    "MAINE": "ME",
    "MARYLAND": "MD",
    "MASSACHUSETTS": "MA",
    "MICHIGAN": "MI",
    "MINNESOTA": "MN",
    "MISSISSIPPI": "MS",
    "MISSOURI": "MO",
    "MONTANA": "MT",
    "NEBRASKA": "NE",
    "NEVADA": "NV",
    "NEWHAMPSHIRE": "NH",
    "NEWJERSEY": "NJ",
    "NEWMEXICO": "NM",
    "NEWYORK": "NY",
    "NORTHCAROLINA": "NC",
    "NORTHDAKOTA": "ND",
    "OHIO": "OH",
    "OKLAHOMA": "OK",
    "OREGON": "OR",
    "PENNSYLVANIA": "PA",
    "RHODEISLAND": "RI",
    "SOUTHCAROLINA": "SC",
    "SOUTHDAKOTA": "SD",
    "TENNESSEE": "TN",
    "TEXAS": "TX",
    "UTAH": "UT",
    "VERMONT": "VT",
    "VIRGINIA": "VA",
    "WASHINGTON": "WA",
    "WESTVIRGINIA": "WV",
    "WISCONSIN": "WI",
    "WYOMING": "WY",
}

# return 10 digit phone number or None
# remove non digit
# leading 0, some have country code 1- or +1
# some have extension's x1234 
#TODO for sake of time moving on 019.126.3340 seems to be an edge case with a valid leading 0, row 37 + 5 
def clean_phone_number(input_number: str) -> str | None:
    """"
    return a valid phone number or None
    """
    built_number = []

    for i in range(len(input_number)):
        # skip leading +1 
        if input_number[i].isdigit() == False and input_number[i+1] == '+':
            continue
        # skip leading 1- 
        elif len(built_number) == 0 and input_number[i] == "1"  and input_number[i+1] == '-':
            continue
        # drop extensions 
        elif input_number[i] == 'x':
            break
        # skip non digit
        elif input_number[i].isdigit() == False:
            continue
        # skip leading 0
        elif input_number[i] == '0' and len(built_number) == 0:
            continue
        # append any other digit
        else:
            built_number.append(input_number[i])

    if len(built_number) == 10:
        return int(''.join(built_number))
    

def clean_email(input_email: str) -> str | None:
    """ Currently just returns the input email OR None """
    if input_email:
        return input_email 
    else:
        return None
    
def clean_city(input_city: str) -> str | None:
    """ Currently just returns the input city OR None """
    if input_city:
        return input_city
    else:
        return None
    
def clean_post_code(input_post_code: str ) -> int | None:
    """ Currently just replaces the INVALID and empty strings with None """
    if input_post_code and input_post_code != 'INVALID' :
        return int(input_post_code)
    else:
        return None

def normalize_text(input_text: str) -> str:
    """ 
    Normalize the text by removing any NON alphabetical characters and converting to uppercase
    """
    input_text = input_text.upper()
    input_text = re.sub(r'[^A-Z]', '', input_text)
    return input_text
    

def clean_country(input_country: str) -> str | None:
    """Matches the different county variations to a single format, since this can miss cases, it will log the missed cases to a file"""

    if not input_country:
        return None
    
    input_country = normalize_text(input_country)
    if input_country in country_map:
        return country_map[input_country]
    else:
        with open('invalid_countries.txt', 'a') as file:
            file.write(f"{input_country}\n")
        return None


def clean_state_initial(input_state: str) -> str | None:
    """Matches the different state variations to a single format, since this can miss cases, it will log the missed cases to a file"""

    if not input_state:
        return None
    
    input_state = normalize_text(input_state)
    # assume the state is a valid 2 letter state code
    if len(input_state) == 2:
        return input_state
    elif input_state in state_map:
        return state_map[input_state]
    else:
        with open('invalid_states.txt', 'a') as file:
            file.write(f"{input_state}\n")
        return None

def clean_shipping_address(input_address: str) -> str | None:
    """ Currently just returns the input address OR None """
    if input_address:
        return input_address
    else:
        return None

def clean_date(input_date: str) -> str | None:
    """ standardize the date format to YYYY-MM-DD"""
    if not input_date:
        return None
    else:
        try:
            parsed_date = parse(input_date)
            return parsed_date.strftime('%Y-%m-%d')
        except ValueError:
            return None
        
def clean_price(input_price: str) -> float | None:
    """ removes the $ sign """
    input_price = re.sub(r'[^\d.]', '', input_price)
    return float(input_price)
    

def insert_customer(row):
    insert_customer_query(connection, row)

def insert_order(row):
    insert_order_query(connection, row)

def insert_product(row):
    insert_product_query(connection, row)
    

def start(data_dir: Path):
    # print(f"Data directory: {data_dir}")

    customers_file = data_dir / 'customers.csv'
    orders_file = data_dir / 'orders.csv'
    products_file = data_dir / 'products.csv'

    with customers_file.open('r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader) #skip the header

        for row in csv_reader:
            if len(row) < 10:
                print(f"Error, row {row} is missing columns")
                continue

            row[3] = clean_email(row[3])
            row[4] = clean_phone_number(row[4])
            row[6] = clean_city(row[6])
            row[8] = clean_post_code(row[8])

            insert_customer(row)
            
   
    with orders_file.open('r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader) #skip the header

        for row in csv_reader:
            if len(row) < 11:
                print(f"Error, row {row} is missing columns")
                continue

            row[3] = clean_date(row[3])
            row[4] = clean_date(row[4])
            row[6] = clean_shipping_address(row[6])
            row[7] = clean_city(row[7])
            row[8] = clean_state_initial(row[8])
            row[9] = clean_post_code(row[9])
            row[10] = clean_country(row[10])

            insert_order(row)

    with products_file.open('r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader) #skip the header

        for row in csv_reader:
            if len(row) < 3:
                print(f"Error, row {row} is missing columns")
                continue
            
            row[2] = clean_price(row[2])

            insert_product(row)

    
# this is the entry point of the script
if __name__ == '__main__':
    data_dir = Path.cwd() / 'data'

    connection = get_connection()
    start(data_dir=data_dir)