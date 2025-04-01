import abc

import sqlalchemy

from scs.core.db.models.mixins.id_mixin import IdMixin


class IdRepoMixin[T: IdMixin](abc.ABC):
    session = sqlalchemy.orm.Session

    def find_by_id(self, id: int) -> T | None:
        return self.session.execute(
                sqlalchemy.select(T).filter_by(id=id)
        ).scalars().one_or_none()
