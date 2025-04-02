from sqlalchemy.orm import Session

from scs.core.db.models.item_models.bought_item_orm import BoughtItemORM
from scs.core.repos.mixins.id_repo_mixin import IdRepoMixin


class BoughtItemRepository(IdRepoMixin[BoughtItemORM]):
    def __init__(self, session: Session):
        self.session = session
