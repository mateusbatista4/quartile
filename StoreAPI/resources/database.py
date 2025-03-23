from flask import current_app, g
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_app(app):
    db.init_app(app)
    
    @app.teardown_appcontext
    def close_db(e=None):
        if hasattr(g, 'db_session'):
            g.db_session.close()

def get_db():
    return db

def create_tables():
    db.create_all()
    
def drop_tables():
    db.drop_all()
    
def reset_db():
    drop_tables()
    create_tables() 