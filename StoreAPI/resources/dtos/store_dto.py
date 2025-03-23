from dataclasses import dataclass, asdict
from typing import List, Optional, Dict, Any

@dataclass
class StoreDTO:
    id: int
    name: str
    address: str
    company_id: int
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    phone: Optional[str] = None
    
    @classmethod
    def from_entity(cls, store_entity: Dict[str, Any]) -> 'StoreDTO':
        return cls(
            id=store_entity.get('id'),
            name=store_entity.get('name'),
            address=store_entity.get('address'),
            company_id=store_entity.get('company_id'),
            city=store_entity.get('city'),
            state=store_entity.get('state'),
            postal_code=store_entity.get('postal_code'),
            phone=store_entity.get('phone')
        )
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
    
    def to_response(self, include_links: bool = True) -> Dict[str, Any]:
        response = {
            'data': self.to_dict()
        }
        
        if include_links:
            response['links'] = {
                'self': f"/api/stores/{self.id}",
                'company': f"/api/companies/{self.company_id}",
                'company_stores': f"/api/companies/{self.company_id}/stores"
            }
            
        return response


class StoreListDTO:
    @staticmethod
    def create_paginated_response(
        stores: List[Dict[str, Any]], 
        page: int, 
        per_page: int,
        total: int,
        query_params: str = "",
        base_url: str = "/api/stores"
    ) -> Dict[str, Any]:
        store_dtos = [StoreDTO.from_entity(store).to_dict() for store in stores]
        
        total_pages = (total + per_page - 1) // per_page
        
        response = {
            'data': store_dtos,
            'metadata': {
                'page': page,
                'per_page': per_page,
                'total': total,
                'pages': total_pages
            },
            'links': {
                'self': f"{base_url}?page={page}&{query_params}"
            }
        }
        
        if page > 1:
            response['links']['prev'] = f"{base_url}?page={page-1}&{query_params}"
        if page < total_pages:
            response['links']['next'] = f"{base_url}?page={page+1}&{query_params}"
            
        return response 