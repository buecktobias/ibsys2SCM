from sqlalchemy.orm import Session

from scs.core.db.models.item_models import BoughtItemORM
from scs.core.repos.mixins.find_by_id import FindById


class BoughtItemRepository(FindById[BoughtItemORM]):
    def __init__(self, session: Session):
        self.session = session
