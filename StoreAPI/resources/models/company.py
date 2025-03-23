from resources.database import get_db

db = get_db()

class Company(db.Model):
    __tablename__ = 'companies'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    document_number = db.Column(db.String(30), nullable=False, unique=True)
    country = db.Column(db.String(100), default="Brazil")
    address = db.Column(db.String(255))
    contact_email = db.Column(db.String(100))
    contact_phone = db.Column(db.String(20))
    
    stores = db.relationship('Store', backref='company', lazy=True, cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "document_number": self.document_number,
            "country": self.country,
            "address": self.address,
            "contact_email": self.contact_email,
            "contact_phone": self.contact_phone,
            "stores_count": len(self.stores) if self.stores else 0
        } 