import abc

import sqlalchemy

from scs.core.db.models.base import IdMixin


class FindById[T: IdMixin](abc.ABC):
    session = sqlalchemy.orm.Session

    def find_by_id(self, id: str) -> T | None:
        return self.session.execute(
                sqlalchemy.select(T).filter_by(id=id)
        ).scalars().one_or_none()
