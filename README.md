# Quartile Microservices

This repository contains two API microservices that power the Quartile application:

1. **StoreAPI**: A Python-based API for managing companies and their stores
2. **ProductAPI**: A C# Azure Functions serverless API for managing product data

## Project Structure

- `/StoreAPI`: Python backend for company and store management
- `/ProductAPI`: C# Azure Functions for product management

## Deployed Services

- **StoreAPI**: https://the-quartile-api.azurewebsites.net/
- **ProductAPI**: https://quartile-func.azurewebsites.net/ (May experience intermittent availability)

## Postman Collection

The repository includes a comprehensive Postman collection file (`Quartile Challenge.postman_collection.json`) that contains pre-configured requests for both APIs:

- **Python API - Manage Stores**: Contains requests for the StoreAPI endpoints:
  - Company operations (GET, POST, PUT, DELETE)
  - Store operations (GET, POST, PUT, DELETE)
  - Company-Store relationship operations

- **C# Functions - Products API**: Contains requests for the ProductAPI endpoints:
  - Product operations (GET, POST, PUT, DELETE)

To use the collection:
1. Import the `Quartile Challenge.postman_collection.json` file into Postman
2. Set the environment variables:
   - `base_url`: https://the-quartile-api.azurewebsites.net (for StoreAPI)
   - `functions_url`: https://quartile-func.azurewebsites.net (for ProductAPI)

The collection includes tests for verifying response status codes and sample request bodies for creating and updating resources.

## StoreAPI Summary

The StoreAPI is a Python-based backend that provides endpoints for managing companies and their associated stores.

### Key Features
- Full CRUD operations for companies and stores
- Relationship management between companies and their stores
- Interactive API documentation with Swagger UI
- CORS support

### Documentation
- Local: http://localhost:5535/docs
- Deployed: https://the-quartile-api.azurewebsites.net/docs

## ProductAPI Summary

The ProductAPI is a C# serverless microservice built with Azure Functions for managing product data.

### Key Features
- Full CRUD operations for products
- Serverless architecture using Azure Functions
- SQL Server data storage
- Proper data validation
- Error handling with appropriate HTTP status codes

### Base Endpoints
- **GET /api/products** - Get all products
- **GET /api/products/{id}** - Get product by ID
- **POST /api/products** - Create new product
- **PUT /api/products/{id}** - Update product
- **DELETE /api/products/{id}** - Delete product

## Getting Started

Please refer to the README files in each project directory for detailed setup instructions:
- [StoreAPI Setup](/StoreAPI/README.md)
- [ProductAPI Setup](/ProductAPI/README.md)

## Technologies Used

- **StoreAPI**: Python, Flask, SQL Server
- **ProductAPI**: C#, .NET 6, Azure Functions, SQL Server

## Testing

Each project contains its own testing framework and instructions. 