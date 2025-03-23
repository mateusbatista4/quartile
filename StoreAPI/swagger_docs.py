def swagger_definitions():
    """Return Swagger definitions for models"""
    return {
        "Company": {
            "type": "object",
            "properties": {
                "id": {
                    "type": "integer",
                    "format": "int64"
                },
                "name": {
                    "type": "string"
                },
                "document_number": {
                    "type": "string"
                },
                "country": {
                    "type": "string"
                },
                "address": {
                    "type": "string"
                },
                "contact_email": {
                    "type": "string"
                },
                "contact_phone": {
                    "type": "string"
                }
            }
        },
        "Store": {
            "type": "object",
            "properties": {
                "id": {
                    "type": "integer",
                    "format": "int64"
                },
                "name": {
                    "type": "string"
                },
                "address": {
                    "type": "string"
                },
                "city": {
                    "type": "string"
                },
                "state": {
                    "type": "string"
                },
                "postal_code": {
                    "type": "string"
                },
                "phone": {
                    "type": "string"
                },
                "company_id": {
                    "type": "integer",
                    "format": "int64"
                }
            }
        },
        "Pagination": {
            "type": "object",
            "properties": {
                "page": {
                    "type": "integer"
                },
                "per_page": {
                    "type": "integer"
                },
                "total": {
                    "type": "integer"
                },
                "pages": {
                    "type": "integer"
                },
                "next": {
                    "type": "string"
                },
                "prev": {
                    "type": "string"
                }
            }
        }
    }

def swagger_paths():
    """Return Swagger paths for all endpoints"""
    return {
        "/api/companies/": {
            "get": {
                "tags": ["Companies"],
                "summary": "Get all companies",
                "description": "Returns a list of companies with pagination",
                "parameters": [
                    {
                        "name": "page",
                        "in": "query",
                        "description": "Page number",
                        "required": False,
                        "type": "integer",
                        "default": 1
                    },
                    {
                        "name": "per_page",
                        "in": "query",
                        "description": "Items per page (max 100)",
                        "required": False,
                        "type": "integer",
                        "default": 10
                    },
                    {
                        "name": "country",
                        "in": "query",
                        "description": "Filter by country",
                        "required": False,
                        "type": "string"
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Successful operation",
                        "schema": {
                            "type": "object",
                            "properties": {
                                "data": {
                                    "type": "array",
                                    "items": {
                                        "$ref": "#/definitions/Company"
                                    }
                                },
                                "pagination": {
                                    "$ref": "#/definitions/Pagination"
                                }
                            }
                        }
                    }
                }
            },
            "post": {
                "tags": ["Companies"],
                "summary": "Create a new company",
                "description": "Creates a new company record",
                "parameters": [
                    {
                        "name": "body",
                        "in": "body",
                        "description": "Company object",
                        "required": True,
                        "schema": {
                            "type": "object",
                            "required": ["name", "document_number"],
                            "properties": {
                                "name": {
                                    "type": "string",
                                    "description": "Company name"
                                },
                                "document_number": {
                                    "type": "string",
                                    "description": "Company document number (e.g. CNPJ)"
                                },
                                "country": {
                                    "type": "string",
                                    "description": "Company country",
                                    "default": "Brazil"
                                },
                                "address": {
                                    "type": "string",
                                    "description": "Company address"
                                },
                                "contact_email": {
                                    "type": "string",
                                    "description": "Contact email"
                                },
                                "contact_phone": {
                                    "type": "string",
                                    "description": "Contact phone number"
                                }
                            }
                        }
                    }
                ],
                "responses": {
                    "201": {
                        "description": "Company created successfully",
                        "schema": {
                            "$ref": "#/definitions/Company"
                        }
                    },
                    "400": {
                        "description": "Invalid input or document number already exists"
                    },
                    "500": {
                        "description": "Server error"
                    }
                }
            }
        },
        "/api/companies/{company_id}": {
            "get": {
                "tags": ["Companies"],
                "summary": "Get a company by ID",
                "description": "Returns a single company",
                "parameters": [
                    {
                        "name": "company_id",
                        "in": "path",
                        "description": "ID of the company",
                        "required": True,
                        "type": "integer"
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Successful operation",
                        "schema": {
                            "$ref": "#/definitions/Company"
                        }
                    },
                    "404": {
                        "description": "Company not found"
                    }
                }
            },
            "put": {
                "tags": ["Companies"],
                "summary": "Update a company",
                "description": "Updates an existing company",
                "parameters": [
                    {
                        "name": "company_id",
                        "in": "path",
                        "description": "ID of the company",
                        "required": True,
                        "type": "integer"
                    },
                    {
                        "name": "body",
                        "in": "body",
                        "description": "Updated company object",
                        "required": True,
                        "schema": {
                            "type": "object",
                            "properties": {
                                "name": {
                                    "type": "string",
                                    "description": "Company name"
                                },
                                "document_number": {
                                    "type": "string",
                                    "description": "Company document number (e.g. CNPJ)"
                                },
                                "country": {
                                    "type": "string",
                                    "description": "Company country"
                                },
                                "address": {
                                    "type": "string",
                                    "description": "Company address"
                                },
                                "contact_email": {
                                    "type": "string",
                                    "description": "Contact email"
                                },
                                "contact_phone": {
                                    "type": "string",
                                    "description": "Contact phone number"
                                }
                            }
                        }
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Company updated successfully",
                        "schema": {
                            "$ref": "#/definitions/Company"
                        }
                    },
                    "400": {
                        "description": "Invalid input or document number already exists"
                    },
                    "404": {
                        "description": "Company not found"
                    },
                    "500": {
                        "description": "Server error"
                    }
                }
            },
            "delete": {
                "tags": ["Companies"],
                "summary": "Delete a company",
                "description": "Deletes a company",
                "parameters": [
                    {
                        "name": "company_id",
                        "in": "path",
                        "description": "ID of the company",
                        "required": True,
                        "type": "integer"
                    }
                ],
                "responses": {
                    "204": {
                        "description": "Company deleted successfully"
                    },
                    "404": {
                        "description": "Company not found"
                    }
                }
            }
        },
        "/api/stores/": {
            "get": {
                "tags": ["Stores"],
                "summary": "Get all stores",
                "description": "Returns a list of stores with pagination",
                "parameters": [
                    {
                        "name": "page",
                        "in": "query",
                        "description": "Page number",
                        "required": False,
                        "type": "integer",
                        "default": 1
                    },
                    {
                        "name": "per_page",
                        "in": "query",
                        "description": "Items per page (max 100)",
                        "required": False,
                        "type": "integer",
                        "default": 10
                    },
                    {
                        "name": "company_id",
                        "in": "query",
                        "description": "Filter by company ID",
                        "required": False,
                        "type": "integer"
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Successful operation",
                        "schema": {
                            "type": "object",
                            "properties": {
                                "data": {
                                    "type": "array",
                                    "items": {
                                        "$ref": "#/definitions/Store"
                                    }
                                },
                                "pagination": {
                                    "$ref": "#/definitions/Pagination"
                                }
                            }
                        }
                    }
                }
            },
            "post": {
                "tags": ["Stores"],
                "summary": "Create a new store",
                "description": "Creates a new store record",
                "parameters": [
                    {
                        "name": "body",
                        "in": "body",
                        "description": "Store object",
                        "required": True,
                        "schema": {
                            "type": "object",
                            "required": ["name", "address", "company_id"],
                            "properties": {
                                "name": {
                                    "type": "string",
                                    "description": "Store name"
                                },
                                "address": {
                                    "type": "string",
                                    "description": "Store address"
                                },
                                "city": {
                                    "type": "string",
                                    "description": "Store city"
                                },
                                "state": {
                                    "type": "string",
                                    "description": "Store state/province"
                                },
                                "postal_code": {
                                    "type": "string",
                                    "description": "Store postal code"
                                },
                                "phone": {
                                    "type": "string",
                                    "description": "Store phone number"
                                },
                                "company_id": {
                                    "type": "integer",
                                    "description": "ID of the company this store belongs to"
                                }
                            }
                        }
                    }
                ],
                "responses": {
                    "201": {
                        "description": "Store created successfully",
                        "schema": {
                            "$ref": "#/definitions/Store"
                        }
                    },
                    "400": {
                        "description": "Invalid input or company not found"
                    },
                    "500": {
                        "description": "Server error"
                    }
                }
            }
        },
        "/api/stores/{store_id}": {
            "get": {
                "tags": ["Stores"],
                "summary": "Get a store by ID",
                "description": "Returns a single store",
                "parameters": [
                    {
                        "name": "store_id",
                        "in": "path",
                        "description": "ID of the store",
                        "required": True,
                        "type": "integer"
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Successful operation",
                        "schema": {
                            "$ref": "#/definitions/Store"
                        }
                    },
                    "404": {
                        "description": "Store not found"
                    }
                }
            },
            "put": {
                "tags": ["Stores"],
                "summary": "Update a store",
                "description": "Updates an existing store",
                "parameters": [
                    {
                        "name": "store_id",
                        "in": "path",
                        "description": "ID of the store",
                        "required": True,
                        "type": "integer"
                    },
                    {
                        "name": "body",
                        "in": "body",
                        "description": "Updated store object",
                        "required": True,
                        "schema": {
                            "type": "object",
                            "properties": {
                                "name": {
                                    "type": "string",
                                    "description": "Store name"
                                },
                                "address": {
                                    "type": "string",
                                    "description": "Store address"
                                },
                                "city": {
                                    "type": "string",
                                    "description": "Store city"
                                },
                                "state": {
                                    "type": "string",
                                    "description": "Store state/province"
                                },
                                "postal_code": {
                                    "type": "string",
                                    "description": "Store postal code"
                                },
                                "phone": {
                                    "type": "string",
                                    "description": "Store phone number"
                                },
                                "company_id": {
                                    "type": "integer",
                                    "description": "ID of the company this store belongs to"
                                }
                            }
                        }
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Store updated successfully",
                        "schema": {
                            "$ref": "#/definitions/Store"
                        }
                    },
                    "404": {
                        "description": "Store not found"
                    },
                    "500": {
                        "description": "Server error"
                    }
                }
            },
            "delete": {
                "tags": ["Stores"],
                "summary": "Delete a store",
                "description": "Deletes a store",
                "parameters": [
                    {
                        "name": "store_id",
                        "in": "path",
                        "description": "ID of the store",
                        "required": True,
                        "type": "integer"
                    }
                ],
                "responses": {
                    "204": {
                        "description": "Store deleted successfully"
                    },
                    "404": {
                        "description": "Store not found"
                    }
                }
            }
        },
        "/api/companies/{company_id}/stores": {
            "get": {
                "tags": ["Companies", "Stores"],
                "summary": "Get stores for a company",
                "description": "Returns a list of stores belonging to a company",
                "parameters": [
                    {
                        "name": "company_id",
                        "in": "path",
                        "description": "ID of the company",
                        "required": True,
                        "type": "integer"
                    },
                    {
                        "name": "page",
                        "in": "query",
                        "description": "Page number",
                        "required": False,
                        "type": "integer",
                        "default": 1
                    },
                    {
                        "name": "per_page",
                        "in": "query",
                        "description": "Items per page (max 100)",
                        "required": False,
                        "type": "integer",
                        "default": 10
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Successful operation",
                        "schema": {
                            "type": "object",
                            "properties": {
                                "data": {
                                    "type": "array",
                                    "items": {
                                        "$ref": "#/definitions/Store"
                                    }
                                },
                                "pagination": {
                                    "$ref": "#/definitions/Pagination"
                                }
                            }
                        }
                    },
                    "404": {
                        "description": "Company not found"
                    }
                }
            }
        }
    }

def get_swagger_spec():
    """Return the complete Swagger specification"""
    return {
        "swagger": "2.0",
        "info": {
            "title": "Stores API for Quartile",
            "description": "API for managing companies and stores",
            "version": "1.0"
        },
        "basePath": "/",
        "schemes": [
            "http",
            "https"
        ],
        "consumes": [
            "application/json"
        ],
        "produces": [
            "application/json"
        ],
        "paths": swagger_paths(),
        "definitions": swagger_definitions()
    } 