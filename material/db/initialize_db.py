from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from converters import GraphConverter
from material.setup.production_graph_setup import create_full_production_graph
from models import Base

if __name__ == '__main__':
    engine = create_engine("sqlite:///manufacturing.db")
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    for table in reversed(Base.metadata.sorted_tables):
        session.execute(table.delete())

    converter = GraphConverter(session)
    converter.add_graph(create_full_production_graph())
