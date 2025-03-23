from flask import abort, request
from flask_restful import Resource, reqparse
from resources.repositories.store_repository import StoreRepository
from resources.dtos.store_dto import StoreDTO, StoreListDTO

# Parser for store creation
store_parser = reqparse.RequestParser()
store_parser.add_argument("name", type=str, help="Store name is required", required=True)
store_parser.add_argument("address", type=str, help="Store address is required", required=True)
store_parser.add_argument("city", type=str)
store_parser.add_argument("state", type=str)
store_parser.add_argument("postal_code", type=str)
store_parser.add_argument("phone", type=str)
store_parser.add_argument("company_id", type=int, help="Company ID is required", required=True)

# Parser for store update (all fields optional)
store_update_parser = reqparse.RequestParser()
store_update_parser.add_argument("name", type=str)
store_update_parser.add_argument("address", type=str)
store_update_parser.add_argument("city", type=str)
store_update_parser.add_argument("state", type=str)
store_update_parser.add_argument("postal_code", type=str)
store_update_parser.add_argument("phone", type=str)
store_update_parser.add_argument("company_id", type=int)

class StoreResource(Resource):
    def post(self):
        store_repo = StoreRepository()
        args = store_parser.parse_args()
        
        saved_store, error = store_repo.save_store(args)
        if not saved_store:
            return {"status": "error", "message": error or "Error saving store"}, 400 if error and "not found" in str(error) else 500
            
        store_dto = StoreDTO.from_entity(saved_store)
        return store_dto.to_response(), 201
        
    def get(self):
        store_repo = StoreRepository()
        
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        company_id = request.args.get('company_id', type=int)
        
        if per_page > 100:
            per_page = 100
        
        if company_id:
            stores = store_repo.get_stores_by_company_id(company_id)
        else:
            stores = store_repo.get_all_stores()
        
        total = len(stores)
        
        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page
        paginated_stores = stores[start_idx:end_idx]
        
        query_params = f"per_page={per_page}"
        if company_id:
            query_params += f"&company_id={company_id}"
        
        response = StoreListDTO.create_paginated_response(
            paginated_stores,
            page,
            per_page,
            total,
            query_params
        )
            
        return response, 200

class StoreDetailResource(Resource):
    def get(self, store_id):
        store_repo = StoreRepository()
        store = store_repo.get_store_by_id(store_id)
        
        if not store:
            return {"status": "error", "message": "Store not found"}, 404
        
        store_dto = StoreDTO.from_entity(store)
        return store_dto.to_response(), 200
        
    def put(self, store_id):
        store_repo = StoreRepository()
        args = store_update_parser.parse_args()
        
        update_data = {k: v for k, v in args.items() if v is not None}
        
        updated_store, error = store_repo.update_store(store_id, update_data)
        if not updated_store:
            if error and "not found" in error:
                return {"status": "error", "message": error}, 404
            return {"status": "error", "message": error or "Error updating store"}, 500
            
        store_dto = StoreDTO.from_entity(updated_store)
        return store_dto.to_response(), 200
        
    def delete(self, store_id):
        store_repo = StoreRepository()
        result = store_repo.delete_store(store_id)
        
        if not result:
            return {"status": "error", "message": "Store not found"}, 404
            
        return {"status": "success", "message": "Store deleted successfully"}, 204

class CompanyStoresResource(Resource):
    def get(self, company_id):
        store_repo = StoreRepository()
        
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        if per_page > 100:
            per_page = 100
            
        stores = store_repo.get_stores_by_company_id(company_id)
        
        total = len(stores)
        
        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page
        paginated_stores = stores[start_idx:end_idx]
        
        response = StoreListDTO.create_paginated_response(
            paginated_stores,
            page,
            per_page,
            total,
            f"per_page={per_page}",
            f"/api/companies/{company_id}/stores"
        )
            
        return response, 200 