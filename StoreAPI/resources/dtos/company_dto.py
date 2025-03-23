from dataclasses import dataclass, asdict
from typing import List, Optional, Dict, Any

@dataclass
class CompanyDTO:
    id: int
    name: str
    document_number: str
    country: str
    address: Optional[str] = None
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    stores_count: int = 0
    
    @classmethod
    def from_entity(cls, company_entity: Dict[str, Any]) -> 'CompanyDTO':
        return cls(
            id=company_entity.get('id'),
            name=company_entity.get('name'),
            document_number=company_entity.get('document_number'),
            country=company_entity.get('country', 'Brazil'),
            address=company_entity.get('address'),
            contact_email=company_entity.get('contact_email'),
            contact_phone=company_entity.get('contact_phone'),
            stores_count=company_entity.get('stores_count', 0)
        )
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
    
    def to_response(self, include_links: bool = True) -> Dict[str, Any]:
        response = {
            'data': self.to_dict()
        }
        
        if include_links:
            response['links'] = {
                'self': f"/api/companies/{self.id}",
                'stores': f"/api/companies/{self.id}/stores"
            }
            
        return response


class CompanyListDTO:
    @staticmethod
    def create_paginated_response(
        companies: List[Dict[str, Any]], 
        page: int, 
        per_page: int,
        total: int,
        query_params: str = ""
    ) -> Dict[str, Any]:
        company_dtos = [CompanyDTO.from_entity(company).to_dict() for company in companies]
        
        total_pages = (total + per_page - 1) // per_page
        
        response = {
            'data': company_dtos,
            'metadata': {
                'page': page,
                'per_page': per_page,
                'total': total,
                'pages': total_pages
            },
            'links': {
                'self': f"/api/companies?page={page}&{query_params}"
            }
        }
        
        if page > 1:
            response['links']['prev'] = f"/api/companies?page={page-1}&{query_params}"
        if page < total_pages:
            response['links']['next'] = f"/api/companies?page={page+1}&{query_params}"
            
        return response 