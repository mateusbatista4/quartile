IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[Products]') AND type in (N'U'))
BEGIN
    CREATE TABLE [dbo].[Products] (
        [id] INT IDENTITY(1,1) PRIMARY KEY,
        [name] NVARCHAR(100) NOT NULL,
        [description] NVARCHAR(500) NULL,
        [price] DECIMAL(18, 2) NOT NULL,
        [stock_quantity] INT NOT NULL,
        [created_date] DATETIME2 NOT NULL,
        [modified_date] DATETIME2 NULL
    )
END 