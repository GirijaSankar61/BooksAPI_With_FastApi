import sqlalchemy

DATABASE_URL = "sqlite:///books.db"

metadata = sqlalchemy.MetaData()
books = sqlalchemy.Table(
    "books",
    metadata,
    sqlalchemy.Column("book_id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String),
    sqlalchemy.Column("author", sqlalchemy.String),
    sqlalchemy.Column("link", sqlalchemy.String),
    sqlalchemy.Column("pages", sqlalchemy.Integer),
)

engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
metadata.create_all(engine)