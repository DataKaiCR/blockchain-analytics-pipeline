from sqlalchemy import create_engine

db_name = 'blockchain'
db_user = 'admin'
db_pass = 'admin'
db_host = 'localhost'
db_port = '7777'

# Connecto to the database

def postgres_connect():
    db_string = 'postgresql://{}:{}@{}:{}/{}'.format(db_user, db_pass, db_host, db_port, db_name)
    db = create_engine(db_string)
    return db