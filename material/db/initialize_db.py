from sqlmodel import SQLModel, create_engine, Session

if __name__ == '__main__':
    engine = create_engine("sqlite:///manufacturing.db")
    SQLModel.metadata.create_all(engine)
