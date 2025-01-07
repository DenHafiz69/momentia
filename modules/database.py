import sqlalchemy as db

# Database setup
engine = db.create_engine("sqlite:///../data/database.db", echo=True)  # Correcting the typo in "sqlitee"
connection = engine.connect()
metadata = db.MetaData()

# Table definition
user_table = db.Table(
    "user",
    metadata,
    db.Column("id", db.Integer, primary_key=True),
    db.Column("username", db.String),
    db.Column("email", db.String),
    db.Column("password", db.String)
)

# Create the table in the database
metadata.create_all(engine)

# Functions for interacting with the database
def insert_user(username: str, email: str, password: str) -> None:
    query = user_table.insert().values(username=username, email=email, password=password)
    connection.execute(query)

def select_user(username: str) -> db.engine.Row:
    query = user_table.select().where(user_table.c.username == username)
    result = connection.execute(query)
    return result.fetchone()
    
def main() -> None:
    metadata.create_all(engine)
    connection.close()

if __name__ == "__main__":
    main()