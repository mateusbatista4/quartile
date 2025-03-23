from flask import Flask, jsonify
from flask_restful import Api
from flask_cors import CORS
from resources.api.company import CompanyResource, CompanyDetailResource
from resources.api.store import StoreResource, StoreDetailResource, CompanyStoresResource
from resources.constants import SQLALCHEMY_DATABASE_URI, SERVER, DATABASE, DB_USERNAME, DB_PASSWORD
from resources.database import db, init_app
from flask_swagger_ui import get_swaggerui_blueprint
from swagger_docs import get_swagger_spec
import threading
import pyodbc
import time
import os

app = Flask(__name__)
CORS(app)
api = Api(app)

app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

init_app(app)

SWAGGER_URL = '/docs' 
API_URL = '/swagger'  
@app.route(API_URL)
def get_swagger():
    return jsonify(get_swagger_spec())

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "My API for Quartile"
    }
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

@app.route('/', methods=['GET'])
def api_root():
    return jsonify({
        'api_version': '1.0',
        'resources': {
            'consults': '/api/consults',
            'companies': '/api/companies',
            'stores': '/api/stores',
            'documentation': SWAGGER_URL
        }
    })

api.add_resource(CompanyResource, "/api/companies/")
api.add_resource(CompanyDetailResource, "/api/companies/<int:company_id>")

api.add_resource(StoreResource, "/api/stores/")
api.add_resource(StoreDetailResource, "/api/stores/<int:store_id>")
api.add_resource(CompanyStoresResource, "/api/companies/<int:company_id>/stores")

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'error': 'Not found',
        'message': 'The requested resource was not found'
    }), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({
        'error': 'Internal server error',
        'message': 'An unexpected error occurred'
    }), 500

@app.before_first_request
def create_tables():
    db.create_all()
    
    
def keep_database_active():
    """Function to maintain db alive (Azure shut it off after some time)."""
    conn_str = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SERVER};DATABASE={DATABASE};UID={DB_USERNAME};PWD={DB_PASSWORD}"
    
    while True:
        try:
            with pyodbc.connect(conn_str) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT 1")
                print("[KEEP DATABASE ALIVE] Consult successfully executed.")
        except Exception as e:
            print(f"[KEEP DATABASE ALIVE] Error : {e}")
        
        time.sleep(600) 

thread = threading.Thread(target=keep_database_active, daemon=True)
thread.start()

if __name__ == "__main__":
    app.run(port=5535)#, debug=True)