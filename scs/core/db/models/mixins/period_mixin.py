from sqlalchemy.orm import Mapped, mapped_column


class PeriodMixin:
    """
    Provides functionality for managing and representing a period.

    This mixin class is designed to be used with SQLAlchemy ORM to manage entities
    that require a period column. The 'period' attribute is defined as the primary
    key. This mixin can be inherited by other classes to share period-related
    functionality.

    Attributes:
        period (int): Represents the period, acting as the primary key in the
            table.
    """
    period: Mapped[int] = mapped_column(primary_key=True)
