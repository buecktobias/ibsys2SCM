from sqlalchemy import create_engine

engine = create_engine("postgresql+psycopg://postgres:secret@localhost:6543/postgres")
