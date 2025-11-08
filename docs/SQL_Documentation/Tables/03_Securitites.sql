USE [ETFHoldings]
GO

-- Ensures that NULL comparisons behave according to the ANSI SQL standard (IS NULL must be used) and provides consistent behavior across queries and table scripts.
SET ANSI_NULLS ON
GO

-- Ensures double quotes can be used for table/column names, keeps scripts ANSI-compliant, and is required for some SQL Server features like indexed views and computed columns.
SET QUOTED_IDENTIFIER ON
GO


CREATE TABLE [dbo].[Securities](
	[security_id] [int] IDENTITY(1,1) NOT NULL,
	[symbol] [varchar](10) NOT NULL,
	[name] [varchar](300) NULL,
	[sedol] [varchar](10) NULL,
	[security_type] [varchar](50) NULL,
PRIMARY KEY CLUSTERED 
(
	[security_id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY],
 CONSTRAINT [UQ_Securities_SymbolSedol] UNIQUE NONCLUSTERED 
(
	[symbol] ASC,
	[sedol] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO


