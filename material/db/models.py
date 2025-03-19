from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


### Workstation ###
class Workstation(Base):
    __tablename__ = "workstation"
    workstation_id = Column(Integer, primary_key=True)


### Item (Base Class) ###
class Item(Base):
    __tablename__ = "item"
    item_id = Column(Integer, primary_key=True)

    __mapper_args__ = {
        "polymorphic_identity": "item",
        "polymorphic_on": None,
    }


### BoughtItem ###
class BoughtItem(Item):
    __tablename__ = "bought_item"
    item_id = Column(Integer, ForeignKey("item.item_id"), primary_key=True)
    base_price = Column(Float)
    discount_amount = Column(Integer)
    discount_percentage = Column(Integer)
    mean_order_duration_in_periodes = Column(Float)
    mean_order_standard_deviation_in_periodes = Column(Float)

    __mapper_args__ = {
        "polymorphic_identity": "bought_item",
    }


### ProducedItem ###
class ProducedItem(Item):
    __tablename__ = "produced_item"
    item_id = Column(Integer, ForeignKey("item.item_id"), primary_key=True)

    __mapper_args__ = {
        "polymorphic_identity": "produced_item",
    }


### FullProducedItem ###
class FullProducedItem(ProducedItem):
    __tablename__ = "full_produced_item"
    item_id = Column(Integer, ForeignKey("produced_item.item_id"), primary_key=True)
    base_value_price = Column(Float)

    __mapper_args__ = {
        "polymorphic_identity": "full_produced_item",
    }


### PrimaryItem ###
class PrimaryItem(FullProducedItem):
    __tablename__ = "primary_item"
    item_id = Column(Integer, ForeignKey("full_produced_item.item_id"), primary_key=True)
    sell_price = Column(Float)

    __mapper_args__ = {
        "polymorphic_identity": "primary_item",
    }


### StepProduced ###
class StepProduced(Item):
    __tablename__ = "step_produced"
    item_id = Column(Integer, ForeignKey("item.item_id"), primary_key=True)
    parent_item_id = Column(Integer, ForeignKey("full_produced_item.item_id"), nullable=False)

    __mapper_args__ = {
        "polymorphic_identity": "step_produced",
    }


### Process ###
class Process(Base):
    __tablename__ = "process"

    process_id = Column(Integer, primary_key=True)
    workstation_id = Column(Integer, ForeignKey("workstation.workstation_id"))
    process_duration_in_mins = Column(Integer)
    setup_duration_in_mins = Column(Integer)

    workstation = relationship("Workstation")


### Process Input ###
class ProcessInput(Base):
    __tablename__ = "process_input"

    process_id = Column(Integer, ForeignKey("process.process_id"), primary_key=True)
    item_id = Column(Integer, ForeignKey("item.item_id"), primary_key=True)
    quantity = Column(Integer)


### Process Output ###
class ProcessOutput(Base):
    __tablename__ = "process_output"

    process_id = Column(Integer, ForeignKey("process.process_id"), primary_key=True)
    item_id = Column(Integer, ForeignKey("item.item_id"), primary_key=True)
