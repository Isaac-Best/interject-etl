
Just my notes I made along the way + my time logs 


# Step 1. Setup Environment: 21 minutes 
- wait for downloads + restart PC 
- watch some youtube's on getting started with SMSS + express in order to make DB, it is a local DB 

# Step 2. Get a copy of the Projec: 0 minutes 
- Skipped given a copy of distribution 

# Step 3. Understand the Source Data Files: 22 minutes 

Customers.csv 
- Customer ID looks like a good PK 
- some emails are missing 
- phone number has varying format, some I don't recognize and some are missing 
- some missing cities 
- Postal codes have a few invalid fields 
- country is all USA 

Orders.csv 
- orderID looks like a good PK 
- looks like it has productID this could be a FK 
- has customerID this could be a FK 
- order date differing formats mm-dd-YYYY + YYYY-mm-dd and even strings + missing values 
- ship date same issues as order date 
- order amount -> floats -> Normalization ?? is there only one item per order?? 
- shipping address has missing values 
- Some cities are abbrieviated we'll want these to = the same thing 
- State some are initials, some are the full name, some have extra junk data 
- some postal codes are missing 
- country, some are missing, some are different formats -> we may not need since its alr in customers -> 
unless this is different customer location vs shipping destination country 

some looking up of what actually needs to be cleaned -> looks like some of the standard ones are 
- keep units consistent, abbreviations (state etc), same date types (maybe ISO?), phone numbers 
- missing values -> Can just put Null missing values seem optional 
- normalize data -> drop redundant data  

-> interesting note the addresses in orders are NOT customer addresses on file -> will just assume they are ordering to a different location for now, 
I was considering dropping redundant data but that is not the case it seems 

# Step 4. Setup SQL Server Table: 17 minutes 

In the DDL.sql file
- products.csv + orders.csv prices and products don't line up -> normally I would add a intersection table
but it seems only one item is in the order information and its missing the rest 


# Step 5. Build Ingestion Functionality: 2:30 minutes
- needed to brush up on some basics 
- there are some edge cases I had to skip due to time -> leading 0 as a valid phone number
- little bit of hardcoding here 

# Step 6. Setup a Stored Procedure for Data Verification: 35 minutes 
- maybe I misunderstood this but I had to add a CreatedAt field for this to work -> not ideal 
- haven't writted stored procedure before 

# Step 7. Setup a Stored Procedure for Data Querying: 30 minutes 
- ran over the time limit on this section some queries unfinished -> need to review SQL been about 1 year since used anything involving a join

