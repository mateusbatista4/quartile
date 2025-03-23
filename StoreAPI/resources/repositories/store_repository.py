from resources.models.store import Store, get_db
from resources.models.company import Company
from sqlalchemy.exc import SQLAlchemyError

class StoreRepository:
    def __init__(self):
        self.db = get_db()

    def save_store(self, store_data):
        try:
            company_id = store_data.get("company_id")
            company = self.db.session.query(Company).filter(Company.id == company_id).first()
            if not company:
                return None, "Company not found"
                
            store = Store(
                name=store_data.get("name"),
                address=store_data.get("address"),
                city=store_data.get("city", ""),
                state=store_data.get("state", ""),
                postal_code=store_data.get("postal_code", ""),
                phone=store_data.get("phone", ""),
                company_id=company_id
            )
            
            self.db.session.add(store)
            self.db.session.commit()
            
            return store.to_dict(), None

        except SQLAlchemyError as e:
            self.db.session.rollback()  
            print(f"Error saving store: {str(e)}")
            return None, str(e)

    def get_all_stores(self):
        try:
            stores = self.db.session.query(Store).all()
            return [store.to_dict() for store in stores]
        
        except SQLAlchemyError as e:
            print(f"Error retrieving stores: {str(e)}")
            return []

    def get_stores_by_company_id(self, company_id):
        try:
            stores = self.db.session.query(Store).filter(Store.company_id == company_id).all()
            return [store.to_dict() for store in stores]
        
        except SQLAlchemyError as e:
            print(f"Error retrieving stores for company: {str(e)}")
            return []

    def get_store_by_id(self, store_id):
        try:
            store = self.db.session.query(Store).filter(Store.id == store_id).first()
            return store.to_dict() if store else None
        
        except SQLAlchemyError as e:
            print(f"Error retrieving store: {str(e)}")
            return None

    def update_store(self, store_id, store_data):
        try:
            store = self.db.session.query(Store).filter(Store.id == store_id).first()
            if not store:
                return None, "Store not found"
            
            if "company_id" in store_data:
                company = self.db.session.query(Company).filter(Company.id == store_data["company_id"]).first()
                if not company:
                    return None, "Company not found"
                store.company_id = store_data["company_id"]
            
            if "name" in store_data:
                store.name = store_data["name"]
            if "address" in store_data:
                store.address = store_data["address"]
            if "city" in store_data:
                store.city = store_data["city"]
            if "state" in store_data:
                store.state = store_data["state"]
            if "postal_code" in store_data:
                store.postal_code = store_data["postal_code"]
            if "phone" in store_data:
                store.phone = store_data["phone"]
            
            self.db.session.commit()
            return store.to_dict(), None
            
        except SQLAlchemyError as e:
            self.db.session.rollback()
            print(f"Error updating store: {str(e)}")
            return None, str(e)

    def delete_store(self, store_id):
        try:
            store = self.db.session.query(Store).filter(Store.id == store_id).first()
            if not store:
                return False
                
            self.db.session.delete(store)
            self.db.session.commit()
            return True
            
        except SQLAlchemyError as e:
            self.db.session.rollback()
            print(f"Error deleting store: {str(e)}")
            return False 