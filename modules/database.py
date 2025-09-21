# database_module.py
import sqlalchemy as db
from sqlalchemy.orm import scoped_session, sessionmaker

# Database setup
engine = db.create_engine("sqlite:///./data/database.db", echo=True, connect_args={"check_same_thread": False})
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

post_table = db.Table(
    "post",
    metadata,
    db.Column("id", db.Integer, primary_key=True),
    db.Column("title", db.String, nullable=False),
    db.Column("content", db.Text, nullable=False),
    db.Column("date_posted", db.DateTime, nullable=False, default=db.func.current_timestamp()),
    db.Column("author_id", db.Integer, db.ForeignKey("user.id"), nullable=False),
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

def select_user_by_email(email: str):
    session = Session()
    query = user_table.select().where(user_table.c.email == email)
    result = session.execute(query)
    user = result.fetchone()
    session.close()
    return user

def select_user_by_id(user_id: int):
    session = Session()
    query = user_table.select().where(user_table.c.id == user_id)
    result = session.execute(query)
    user = result.fetchone()
    session.close()
    return user

def update_user(user_id: int, username: str, email: str) -> None:
    session = Session()
    query = user_table.update().where(user_table.c.id == user_id).values(username=username, email=email)
    session.execute(query)
    session.commit()
    session.close()

# Post-related functions
def insert_post(title: str, content: str, author_id: int) -> None:
    session = Session()
    query = post_table.insert().values(title=title, content=content, author_id=author_id)
    session.execute(query)
    session.commit()
    session.close()

def select_all_posts():
    session = Session()
    query = db.select(
        post_table.c.id,
        post_table.c.title,
        post_table.c.content,
        post_table.c.date_posted,
        user_table.c.username.label('author')
    ).select_from(
        post_table.join(user_table, post_table.c.author_id == user_table.c.id)
    ).order_by(post_table.c.date_posted.desc())
    
    result = session.execute(query)
    posts = result.fetchall()
    session.close()
    return posts

def select_post_by_id(post_id: int):
    session = Session()
    query = db.select(
        post_table.c.id,
        post_table.c.title,
        post_table.c.content,
        post_table.c.date_posted,
        post_table.c.author_id,
        user_table.c.username.label('author')
    ).select_from(
        post_table.join(user_table, post_table.c.author_id == user_table.c.id)
    ).where(post_table.c.id == post_id)
    
    result = session.execute(query)
    post = result.fetchone()
    session.close()
    return post

def select_posts_by_user(user_id: int):
    session = Session()
    query = db.select(
        post_table.c.id,
        post_table.c.title,
        post_table.c.content,
        post_table.c.date_posted,
        user_table.c.username.label('author')
    ).select_from(
        post_table.join(user_table, post_table.c.author_id == user_table.c.id)
    ).where(post_table.c.author_id == user_id).order_by(post_table.c.date_posted.desc())
    
    result = session.execute(query)
    posts = result.fetchall()
    session.close()
    return posts

def update_post(post_id: int, title: str, content: str) -> None:
    session = Session()
    query = post_table.update().where(post_table.c.id == post_id).values(title=title, content=content)
    session.execute(query)
    session.commit()
    session.close()

def delete_post(post_id: int) -> None:
    session = Session()
    query = post_table.delete().where(post_table.c.id == post_id)
    session.execute(query)
    session.commit()
    session.close()
