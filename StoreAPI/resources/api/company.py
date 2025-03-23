from flask import abort, request
from flask_restful import Resource, reqparse
from resources.repositories.company_repository import CompanyRepository
from resources.dtos.company_dto import CompanyDTO, CompanyListDTO

# Parser for company creation and update
company_parser = reqparse.RequestParser()
company_parser.add_argument("name", type=str, help="Company name is required", required=True)
company_parser.add_argument("document_number", type=str, help="Document number is required", required=True)
company_parser.add_argument("country", type=str, default="Brazil")
company_parser.add_argument("address", type=str)
company_parser.add_argument("contact_email", type=str)
company_parser.add_argument("contact_phone", type=str)

# Parser for company update (all fields optional)
company_update_parser = reqparse.RequestParser()
company_update_parser.add_argument("name", type=str)
company_update_parser.add_argument("document_number", type=str)
company_update_parser.add_argument("country", type=str)
company_update_parser.add_argument("address", type=str)
company_update_parser.add_argument("contact_email", type=str)
company_update_parser.add_argument("contact_phone", type=str)

class CompanyResource(Resource):
    def post(self):
        company_repo = CompanyRepository()
        args = company_parser.parse_args()
        
        saved_company, error = company_repo.save_company(args)
        if not saved_company:
            if error and "document number already exists" in error:
                return {"status": "error", "message": error}, 400
            return {"status": "error", "message": error or "Error saving company"}, 500
        
        # to dto
        company_dto = CompanyDTO.from_entity(saved_company)
        return company_dto.to_response(), 201
        
    def get(self):
        company_repo = CompanyRepository()
        
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        country = request.args.get('country')
        
        if per_page > 100:
            per_page = 100
            
        companies = company_repo.get_all_companies()
        
        if country:
            companies = [c for c in companies if c.get('country', '').lower() == country.lower()]
        
        total = len(companies)
        
        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page
        paginated_companies = companies[start_idx:end_idx]
        
        query_params = f"per_page={per_page}"
        if country:
            query_params += f"&country={country}"
        
        response = CompanyListDTO.create_paginated_response(
            paginated_companies, 
            page, 
            per_page, 
            total, 
            query_params
        )
            
        return response, 200

class CompanyDetailResource(Resource):
    def get(self, company_id):
        company_repo = CompanyRepository()
        company = company_repo.get_company_by_id(company_id)
        
        if not company:
            return {"status": "error", "message": "Company not found"}, 404
        
        company_dto = CompanyDTO.from_entity(company)
        return company_dto.to_response(), 200
        
    def put(self, company_id):
        company_repo = CompanyRepository()
        args = company_update_parser.parse_args()
        
        update_data = {k: v for k, v in args.items() if v is not None}
        
        updated_company, error = company_repo.update_company(company_id, update_data)
        if not updated_company:
            if error and "not found" in error:
                return {"status": "error", "message": error}, 404
            if error and "document number already exists" in error:
                return {"status": "error", "message": error}, 400
            return {"status": "error", "message": error or "Error updating company"}, 500
        
        company_dto = CompanyDTO.from_entity(updated_company)
        return company_dto.to_response(), 200
        
    def delete(self, company_id):
        company_repo = CompanyRepository()
        result = company_repo.delete_company(company_id)
        
        if not result:
            return {"status": "error", "message": "Company not found"}, 404
            
        return {"status": "success", "message": "Company deleted successfully"}, 204 