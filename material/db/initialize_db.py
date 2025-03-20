from sqlmodel import SQLModel, create_engine, Session

from material.db.converters import GraphConverter
from material.setup.production_graph_setup import create_full_production_graph

if __name__ == '__main__':
    engine = create_engine("sqlite:///scm.db")
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        for table in reversed(SQLModel.metadata.sorted_tables):
            table.delete()
            session.commit()
        converter = GraphConverter(session)
        converter.add_graph(create_full_production_graph())
        session.commit()
