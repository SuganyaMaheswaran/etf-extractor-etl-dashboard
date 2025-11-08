-- Create the database
IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = 'ETFHoldings')
BEGIN
    CREATE DATABASE ETFHoldings;
END
GO

-- Switch to the database
USE ETFHoldings;
GO