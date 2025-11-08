USE [ETFHoldings]
GO

-- Ensures that NULL comparisons behave according to the ANSI SQL standard (IS NULL must be used) and provides consistent behavior across queries and table scripts.
SET ANSI_NULLS ON
GO

-- Ensures double quotes can be used for table/column names, keeps scripts ANSI-compliant, and is required for some SQL Server features like indexed views and computed columns.
SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[ETF_Securities](
	[etf_id] [int] NOT NULL,
	[security_id] [int] NOT NULL,
	[etf_security_id] [int] IDENTITY(1,1) NOT NULL,
 CONSTRAINT [PK_ETF_Securities] PRIMARY KEY CLUSTERED 
(
	[etf_id] ASC,
	[security_id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

ALTER TABLE [dbo].[ETF_Securities]  WITH CHECK ADD FOREIGN KEY([etf_id])
REFERENCES [dbo].[ETFS] ([etf_id])
GO

ALTER TABLE [dbo].[ETF_Securities]  WITH CHECK ADD FOREIGN KEY([security_id])
REFERENCES [dbo].[Securities] ([security_id])
GO


