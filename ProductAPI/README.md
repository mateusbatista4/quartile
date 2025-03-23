# Quartile ProductAPI

This API serves as a backend for managing product data. It provides endpoints for CRUD operations on products, built as a serverless C# microservice with Azure Functions.

## Deployed API
The API is deployed and should be accessible at: https://quartile-func.azurewebsites.net/
Note: The deployed service may experience intermittent availability due to cloud infrastructure issues.

## Getting Started

### Prerequisites
- .NET 6.0 SDK or later
- Azure Functions Core Tools
- SQL Server (local or Azure SQL)
- ODBC Driver 17 for SQL Server

### Installation
1. Clone the repository
2. Install the required dependencies:
```
dotnet restore
```

## Running the API
```
func start
```
The server will start locally and expose the API endpoints.

## Database Setup
Execute the SQL script in the `Data/CreateProductsTable.sql` file to set up the required database table.

## API Documentation
The API uses Swagger for documentation. When running locally, you can access it at the `/docs` endpoint.

## Base Endpoints
- **GET /api/products** - Get all products
- **GET /api/products/{id}** - Get a specific product by ID
- **POST /api/products** - Create a new product
- **PUT /api/products/{id}** - Update an existing product
- **DELETE /api/products/{id}** - Delete a product

## Run Tests
```
dotnet test
```

## Configuration

Update the `local.settings.json` file with your SQL Server connection string:

```json
{
  "IsEncrypted": false,
  "Values": {
    "AzureWebJobsStorage": "UseDevelopmentStorage=true",
    "FUNCTIONS_WORKER_RUNTIME": "dotnet",
    "SqlConnectionString": "Server=localhost;Database=ProductDb;User Id=YOUR_USERNAME;Password=YOUR_PASSWORD;TrustServerCertificate=True"
  }
}
```

## Deployment

To deploy to Azure:

1. Create an Azure Function App resource in the Azure Portal
2. Deploy using the Azure Functions Core Tools:
   ```
   func azure functionapp publish YOUR_FUNCTION_APP_NAME
   ```

3. Configure the application settings in the Azure Portal to include your SQL connection string

## Features
- Full CRUD operations for products
- Serverless architecture using Azure Functions
- Swagger API documentation
- SQL Server data storage
- Proper data validation
- Error handling and appropriate HTTP status codes 