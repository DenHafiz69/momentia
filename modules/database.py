# database_module.py
import sqlalchemy as db
from sqlalchemy.orm import scoped_session, sessionmaker

# Database setup
engine = db.create_engine("sqlite:///:memory:", echo=True, connect_args={"check_same_thread": False})
Session = scoped_session(sessionmaker(bind=engine))

# Metadata and table definition
metadata = db.MetaData()

user_table = db.Table(
    "user",
    metadata,
    db.Column("id", db.Integer, primary_key=True),
    db.Column("username", db.String),
    db.Column("email", db.String),
    db.Column("password", db.String),
)

metadata.create_all(engine)

# Functions for database operations
def insert_user(username: str, email: str, password: str) -> None:
    session = Session()
    query = user_table.insert().values(username=username, email=email, password=password)
    session.execute(query)
    session.commit()
    session.close()

def select_user(username: str):
    session = Session()
    query = user_table.select().where(user_table.c.username == username)
    result = session.execute(query)
    user = result.fetchone()
    session.close()
    return user
