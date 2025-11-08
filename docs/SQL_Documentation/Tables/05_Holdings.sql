USE [ETFHoldings]
GO

-- Ensures that NULL comparisons behave according to the ANSI SQL standard (IS NULL must be used) and provides consistent behavior across queries and table scripts.
SET ANSI_NULLS ON
GO

-- Ensures double quotes can be used for table/column names, keeps scripts ANSI-compliant, and is required for some SQL Server features like indexed views and computed columns.
SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[Holdings](
	[security_str] [varchar](300) NULL,
	[market_val_int] [bigint] NULL,
	[symbol_str] [varchar](10) NULL,
	[sedol_str] [varchar](10) NULL,
	[quantity_int] [bigint] NULL,
	[weight_float] [float] NULL,
	[etf_str] [varchar](10) NULL,
	[update_dt] [date] NULL
) ON [PRIMARY]
GO


