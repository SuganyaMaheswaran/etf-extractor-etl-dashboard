-- Use ETFHoldings
USE [ETFHoldings]
GO

-- Ensures that NULL comparisons behave according to the ANSI SQL standard (IS NULL must be used) and provides consistent behavior across queries and table scripts.
SET ANSI_NULLS ON
GO

-- Ensures double quotes can be used for table/column names, keeps scripts ANSI-compliant, and is required for some SQL Server features like indexed views and computed columns.
SET QUOTED_IDENTIFIER ON
GO

-- Query to create ETFS table 
CREATE TABLE [dbo].[ETFS](
	[etf_id] [int] IDENTITY(1,1) NOT NULL,
	[etf_symbol] [varchar](10) NOT NULL,
	[etf_name] [varchar](255) NULL,
PRIMARY KEY CLUSTERED 
(
	[etf_id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY],
UNIQUE NONCLUSTERED 
(
	[etf_symbol] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO


