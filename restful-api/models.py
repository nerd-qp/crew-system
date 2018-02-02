# coding: utf-8
from crew_api import api, db

##################################################################
### the following code is beautifully generated by sqlacodegen ###
##################################################################

##################################################################
### Some problems with utf-8, some error  ########################
##################################################################

from sqlalchemy import BINARY, Column, Date, DateTime, ForeignKey, ForeignKeyConstraint, Index, Integer, Numeric, SmallInteger, String, Table, Time, text
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql.enumerated import ENUM
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


# t_attr_in_item = Table(
#     'attr_in_item', metadata,
#     Column('attr_ID', ForeignKey('item_attribute.attr_ID'), primary_key=True, nullable=False),
#     Column('item_ID', ForeignKey('training_item.item_ID'), primary_key=True, nullable=False, index=True)
# )

# AttrInItem = Table(
#     'attr_in_item', metadata,
#     Column('attr_ID', ForeignKey('item_attribute.attr_ID'), primary_key=True, nullable=False),
#     Column('item_ID', ForeignKey('training_item.item_ID'), primary_key=True, nullable=False, index=True)
# )

# post bug for sqlacodegen where we have a relationship that has a direct and a secondary relation
class AttrInItem(Base):
     __tablename__ = 'attr_in_item'

     attr_ID = Column(ForeignKey('item_attribute.attr_ID'), primary_key=True, nullable=False)
     item_ID = Column(ForeignKey('training_item.item_ID'), primary_key=True, nullable=False, index=True)


class FeeLog(Base):
    __tablename__ = 'fee_log'

    cost = Column(Numeric(13, 2))
    used_at = Column(DateTime)
    cause = Column(String(200))
    fee_ID = Column(Integer, primary_key=True)


class ItemAttribute(Base):
    __tablename__ = 'item_attribute'

    attr_ID = Column(Integer, primary_key=True)
    attr_name = Column(String(100), unique=True)

    training_item = relationship('TrainingItem', secondary='attr_in_item')


class Member(Base):
    __tablename__ = 'member'

    name = Column(String(20), nullable=False)
    sex = Column(ENUM(u'男', u'女'), server_default=text(u"'男'"))
    enter_club = Column(Date)
    enter_school = Column(Date)
    birth = Column(Date)
    height = Column(SmallInteger)
    weight = Column(SmallInteger)
    ID = Column(Integer, primary_key=True)
    job = Column(ENUM('couch', 'crew leader', 'crew member'), server_default=text("'crew member'"))
    training_level = Column(ENUM('newbie', 'medium', 'old bird'), server_default=text("'newbie'"))

    fee_log = relationship('FeeLog', secondary='paid_by')
    schedule = relationship('Schedule', secondary='schedule_maker')


# t_paid_by = Table(
#     'paid_by', metadata,
#     Column('ID', ForeignKey('member.ID', ondelete='CASCADE'), primary_key=True, nullable=False),
#     Column('fee_ID', ForeignKey('fee_log.fee_ID'), primary_key=True, nullable=False, index=True)
# )

t_paid_by = Table(
    'paid_by', metadata,
    Column('ID', ForeignKey('member.ID', ondelete='CASCADE'), primary_key=True, nullable=False),
    Column('fee_ID', ForeignKey('fee_log.fee_ID'), primary_key=True, nullable=False, index=True)
)



t_record_in_plan = Table(
    'record_in_plan', metadata,
    Column('plan_ID', ForeignKey('training_plan.plan_ID'), primary_key=True, nullable=False),
    Column('record_ID', ForeignKey('training_record.record_ID'), primary_key=True, nullable=False, index=True)
)


class RequirementInPlan(Base):
    __tablename__ = 'requirement_in_plan'
    __table_args__ = (
        ForeignKeyConstraint(['item_ID', 'attr_ID'], ['attr_in_item.item_ID', 'attr_in_item.attr_ID']),
        Index('item_ID', 'item_ID', 'attr_ID')
    )

    plan_ID = Column(ForeignKey('training_plan.plan_ID'), primary_key=True, nullable=False)
    item_ID = Column(Integer, primary_key=True, nullable=False)
    attr_ID = Column(Integer, primary_key=True, nullable=False)
    comp = Column(ENUM('larger', 'smaller', 'no requirement'), nullable=False, server_default=text("'no requirement'"))
    requirement = Column(Integer)

    attr_in_item = relationship('AttrInItem')
    training_plan = relationship('TrainingPlan')


class Schedule(Base):
    __tablename__ = 'schedule'

    add_time = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    happen_at = Column(DateTime)
    event_ID = Column(Integer, primary_key=True)
    event = Column(String(100), nullable=False)
    spec = Column(String(1000))
    length = Column(Time)


t_schedule_maker = Table(
    'schedule_maker', metadata,
    Column('event_ID', ForeignKey('schedule.event_ID'), primary_key=True, nullable=False),
    Column('ID', ForeignKey('member.ID', ondelete='CASCADE'), primary_key=True, nullable=False, index=True)
)


class Ship(Base):
    __tablename__ = 'ship'

    ship_name = Column(String(100), primary_key=True)
    ship_type_ID = Column(ForeignKey('ship_type_table.ship_type_ID'), index=True)
    condition_description = Column(String(1000))

    ship_type_table = relationship('ShipTypeTable')


class ShipTypeTable(Base):
    __tablename__ = 'ship_type_table'

    ship_type_ID = Column(Integer, primary_key=True)
    ship_type_name = Column(String(100))


class StatusInRecord(Base):
    __tablename__ = 'status_in_record'
    __table_args__ = (
        ForeignKeyConstraint(['item_ID', 'attr_ID'], ['attr_in_item.item_ID', 'attr_in_item.attr_ID']),
        Index('item_ID', 'item_ID', 'attr_ID')
    )

    record_ID = Column(ForeignKey('training_record.record_ID'), primary_key=True, nullable=False)
    item_ID = Column(Integer, primary_key=True, nullable=False)
    attr_ID = Column(Integer, primary_key=True, nullable=False)
    status = Column(Integer)

    attr_in_item = relationship('AttrInItem')
    training_record = relationship('TrainingRecord')


class TrainingItem(Base):
    __tablename__ = 'training_item'

    item_name = Column(String(100))
    item_ID = Column(Integer, primary_key=True)
    is_strength = Column(ENUM('y', 'n'))
    is_test = Column(ENUM('y', 'n'))


class TrainingPlan(Base):
    __tablename__ = 'training_plan'

    plan_ID = Column(Integer, primary_key=True)
    train_at = Column(DateTime)
    training_last = Column(Time)
    ID = Column(ForeignKey('member.ID'), index=True)
    training_level = Column(ENUM('newbie', 'medium', 'old bird', 'all'), server_default=text("'all'"))

    member = relationship('Member')
    training_record = relationship('TrainingRecord', secondary='record_in_plan')


class TrainingRecord(Base):
    __tablename__ = 'training_record'

    record_ID = Column(Integer, primary_key=True)
    train_at = Column(DateTime)
    training_last = Column(Time)
    ID = Column(ForeignKey('member.ID'), index=True)

    member = relationship('Member')


class User(Base):
    __tablename__ = 'users'

    username = Column(String(20), primary_key=True)
    password = Column(BINARY(128), nullable=False)
    ID = Column(ForeignKey('member.ID', ondelete='CASCADE'), index=True)
    email = Column(String(50), nullable=False, unique=True)

    member = relationship('Member')

