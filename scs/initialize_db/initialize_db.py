from sqlalchemy import delete
from sqlalchemy.orm import Session

from material.db.config import engine
from material.initialize_db.converters import GraphConverter
from material.initialize_db.setup.production_graph_setup import create_full_production_graph
from material.db.models import Base

if __name__ == "__main__":
    with Session(engine) as session:
        for table in reversed(Base.metadata.sorted_tables):
            session.execute(delete(table))
        session.commit()

        converter = GraphConverter(session)
        converter.add_graph(create_full_production_graph())
        session.commit()
