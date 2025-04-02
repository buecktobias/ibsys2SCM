from sqlalchemy import create_engine

engine = create_engine("postgresql+psycopg:/d/app_user:1234@localhost:6543/postgres")
