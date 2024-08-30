import pyodbc


SERVER = 'LAPTOP-8U57M829\SQLEXPRESS'
DATABASE = 'interject-isaac'

connectionString = f'DRIVER=SQL Server;SERVER={SERVER};DATABASE={DATABASE};"Trusted_Connection=yes;"'


def get_connection():
    connection = None
    try: 
        connection = pyodbc.connect(connectionString)
    except Exception as e:
        print(f"Error, {e} while trying to connect to DB")
    
    return connection


# TODO delete if I don't end up using this 
def reset():
    with get_connection() as connection:
        with connection.cursor() as cursor:
            with open('DDL.sql', 'r') as f:
                for result in cursor.execute(f.read(), multi=True):
                    pass

def insert_customer_query(connection, row):
    try: 
        connection.execute(
            """
            INSERT INTO customers (CustomerID, FirstName, LastName, Email, Phone, Address, City, State, PostalCode, Country)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, row
        )
        connection.commit()
    except Exception as e:
        print(f"Error, {e} while trying to insert customer")

def insert_order_query(connection, row):
    try: 
        connection.execute(
            """
            INSERT INTO orders (OrderID, ProductID, CustomerID, OrderDate, ShipDate, OrderAmount, ShippingAddress, ShippingCity, State, PostalCode, Country)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, row
        )
        connection.commit()
    except Exception as e:
        print(f"Error, {e} while trying to insert order")

def insert_product_query(connection, row):
    try: 
        connection.execute(
            """
            INSERT INTO products (ProductID, ProductName, Price)
            VALUES (?, ?, ?)
            """, row
        )
        connection.commit()
    except Exception as e:
        print(f"Error, {e} while trying to insert product")
        
