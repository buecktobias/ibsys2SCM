import pytest

from scs.core.db.process_models.process_input_orm import ProcessInputORM


@pytest.mark.usefixtures("db_session")
class TestProcessInputORM:

    def test_process_input_creation(self, db_session):
        # Assign
        new_process_input = ProcessInputORM(
                process_id=1,
                item_id=1001,
                quantity=10,
        )

        # Act
        db_session.add(new_process_input)
        db_session.commit()
        retrieved = db_session.query(ProcessInputORM).filter_by(process_id=1).one_or_none()

        # Assert
        assert retrieved is not None
        assert retrieved.process_id == 1
        assert retrieved.quantity == 10

    def test_process_input_cascades_on_delete(self, db_session):
        # Test setup must include creation of related ProcessORM (not implemented).
        # Ensures `ondelete="CASCADE"` works correctly with database handling.
        pass

    def test_process_relationship(self, db_session):
        # Test setup must include creation of related ProcessORM and respective relationship verification.
        pass
