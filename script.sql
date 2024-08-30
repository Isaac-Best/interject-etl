-- You can put your table definitions and stored procedures here or in separate files

DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS customers;


CREATE TABLE customers(
    CustomerID INT PRIMARY KEY,
    FirstName VARCHAR(100),
    LastName VARCHAR(100),
    Email VARCHAR(100),
    Phone VARCHAR(25),
    Address VARCHAR(255),
    City VARCHAR(255),
    State VARCHAR(2),
    PostalCode VARCHAR(10),
    Country VARCHAR(50),
    CreatedAt DATETIME DEFAULT GETDATE(),
);


CREATE TABLE orders (
    OrderID INT PRIMARY KEY,
    ProductID INT,
    CustomerID INT,
    OrderDate DATE,
    ShipDate DATE,
    OrderAmount DECIMAL(10,2),
    ShippingAddress VARCHAR(255),
    ShippingCity VARCHAR(255),
    State VARCHAR(2),
    PostalCode VARCHAR(10),
    Country VARCHAR(20),
    CreatedAt DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (CustomerID) REFERENCES customers(CustomerID) ON DELETE CASCADE,
    FOREIGN KEY (ProductID) REFERENCES products(ProductID)
);

CREATE TABLE products (
    ProductID INT PRIMARY KEY,
    ProductName VARCHAR(255),
    Price DECIMAL(10,2),
    CreatedAt DATETIME DEFAULT GETDATE(),
);

select * from dbo.customers; 
select  * from dbo.orders; 
select * from dbo.products;

CREATE PROCEDURE dataVerification 
    @table_name NVARCHAR(50), 
    @timeStamp DATETIME
AS 
BEGIN
    DECLARE @sql NVARCHAR(MAX);

    SET @sql = N'SELECT COUNT(*) AS RowCount FROM ' + QUOTENAME(@table_name) + ' WHERE CreatedAt >= @timeStamp';

    EXEC sp_executesql @sql, N'@timeStamp DATETIME', @timeStamp;
END
GO

EXEC dataVerification 
    @table_name = 'orders', 
    @timeStamp = '2024-08-29';

EXEC dataVerification 
    @table_name = 'customers', 
    @timeStamp = '2024-08-29';


CREATE PROCEDURE getUserOrders 
    @CustomerID NVARCHAR(50)
AS 
BEGIN
    SELECT * FROM orders WHERE CustomerID = @CustomerID;
END
GO


CREATE PROCEDURE getOrdersByDate 
    @OrderDateStart DATE
    @OrderDateEnd DATE
AS
BEGIN
    SELECT * FROM orders WHERE OrderDate >= @OrderDateStart AND OrderDate <= @OrderDateEnd;

END
GO

