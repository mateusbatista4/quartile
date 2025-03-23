# Quartile API

This API serves as a backend for managing companies and their stores. It provides endpoints for CRUD operations on both companies and stores, with proper relationships between them.

## Getting Started

### Prerequisites
- Python 3.11+
- ODBC Driver 17 for SQL Server

### Installation
1. Clone the repository
2. Install the required dependencies:
```
pip install -r requirements.txt
```

## Running the API
```
python app.py
```
The server will start on port 5535. You can access it at http://localhost:5535

## Deployed API
The API is deployed and accessible at: https://the-quartile-api.azurewebsites.net/

## API Documentation
Browse the interactive Swagger documentation at http://localhost:5535/docs
For the deployed version: https://the-quartile-api.azurewebsites.net/docs

This provides detailed information about all endpoints, required parameters, and responses.

## Base Endpoints
- API Info: `GET /`
- Companies: `GET/POST /api/companies/`
- Company Detail: `GET/PUT/DELETE /api/companies/{company_id}`
- Stores: `GET/POST /api/stores/`
- Store Detail: `GET/PUT/DELETE /api/stores/{store_id}`
- Company Stores: `GET /api/companies/{company_id}/stores`

## Run Tests
```
python -m pytest tests/
```

## Database
The API uses an Azure SQL Server database. The connection is maintained through a background thread that executes a periodic query to prevent Azure from shutting down the database due to inactivity.

## Features
- Full CRUD operations for companies and stores
- Relationship management between companies and their stores
- Interactive API documentation with Swagger UI
- Error handling and appropriate HTTP status codes
- CORS support 