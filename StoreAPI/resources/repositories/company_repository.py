from resources.models.company import Company, get_db
from sqlalchemy.exc import SQLAlchemyError

class CompanyRepository:
    def __init__(self):
        self.db = get_db()

    def save_company(self, company_data):
        try:
            document_number = company_data.get("document_number")
            existing_company = self.db.session.query(Company).filter(Company.document_number == document_number).first()
            
            if existing_company:
                return None, "A company with this document number already exists"
                
            company = Company(
                name=company_data.get("name"),
                document_number=document_number,
                country=company_data.get("country", "Brazil"),
                address=company_data.get("address", ""),
                contact_email=company_data.get("contact_email", ""),
                contact_phone=company_data.get("contact_phone", "")
            )
            
            self.db.session.add(company)
            self.db.session.commit()
            
            return company.to_dict(), None

        except SQLAlchemyError as e:
            self.db.session.rollback()  
            print(f"Error saving company: {str(e)}")
            return None, str(e)

    def get_all_companies(self):
        try:
            companies = self.db.session.query(Company).all()
            return [company.to_dict() for company in companies]
        
        except SQLAlchemyError as e:
            print(f"Error retrieving companies: {str(e)}")
            return []

    def get_company_by_id(self, company_id):
        try:
            company = self.db.session.query(Company).filter(Company.id == company_id).first()
            return company.to_dict() if company else None
        
        except SQLAlchemyError as e:
            print(f"Error retrieving company: {str(e)}")
            return None

    def update_company(self, company_id, company_data):
        try:
            company = self.db.session.query(Company).filter(Company.id == company_id).first()
            if not company:
                return None, "Company not found"
            
            #  check duplicates
            if "document_number" in company_data and company_data["document_number"] != company.document_number:
                existing_company = self.db.session.query(Company).filter(
                    Company.document_number == company_data["document_number"],
                    Company.id != company_id
                ).first()
                
                if existing_company:
                    return None, "A company with this document number already exists"
            
            if "name" in company_data:
                company.name = company_data["name"]
            if "document_number" in company_data:
                company.document_number = company_data["document_number"]
            if "country" in company_data:
                company.country = company_data["country"]
            if "address" in company_data:
                company.address = company_data["address"]
            if "contact_email" in company_data:
                company.contact_email = company_data["contact_email"]
            if "contact_phone" in company_data:
                company.contact_phone = company_data["contact_phone"]
            
            self.db.session.commit()
            return company.to_dict(), None
            
        except SQLAlchemyError as e:
            self.db.session.rollback()
            print(f"Error updating company: {str(e)}")
            return None, str(e)

    def delete_company(self, company_id):
        try:
            company = self.db.session.query(Company).filter(Company.id == company_id).first()
            if not company:
                return False
                
            self.db.session.delete(company)
            self.db.session.commit()
            return True
            
        except SQLAlchemyError as e:
            self.db.session.rollback()
            print(f"Error deleting company: {str(e)}")
            return False 