SERVER = "quartile.database.windows.net"
DATABASE = "db-quartile"
DB_USERNAME = "dbuser"
DB_PASSWORD = ""

SQLITE_DATABASE_URI = "sqlite:///db-quartile.db"

SQLALCHEMY_DATABASE_URI = f"mssql+pyodbc://{DB_USERNAME}:{DB_PASSWORD}@{SERVER}/{DATABASE}?driver=ODBC+Driver+17+for+SQL+Server"