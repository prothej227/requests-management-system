from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    DateTime,
    ForeignKey,
    Text,
    func,
    LargeBinary,
)
from sqlalchemy.orm import relationship
from app.core.database import Base


class Area(Base):
    __tablename__ = "areas"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    logo = Column(LargeBinary, nullable=True)
    requests = relationship("Request", back_populates="area")


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    requests = relationship("Request", back_populates="customer")


class SalesPerson(Base):
    __tablename__ = "sales_persons"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    requests = relationship("Request", back_populates="sales_person")


class Request(Base):
    __tablename__ = "requests"

    id = Column(Integer, primary_key=True, index=True)
    ref_no = Column(String(255), unique=True, index=True, nullable=False)
    date_received = Column(Date, nullable=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=True)
    area_id = Column(Integer, ForeignKey("areas.id"), nullable=True)
    sales_person_id = Column(Integer, ForeignKey("sales_persons.id"), nullable=True)
    short_description = Column(String(255), nullable=True)
    long_description = Column(Text, nullable=True)
    quantity = Column(Integer, nullable=True)
    status = Column(String(50), nullable=True)
    feedback = Column(String(50), nullable=True)
    lpo_no = Column(String(255), nullable=True)
    created_by = Column(String(255), nullable=True)
    created_on = Column(DateTime(timezone=True), server_default=func.now())
    modified_by = Column(String(255), nullable=True)
    modified_on = Column(DateTime(timezone=True), onupdate=func.now())
    customer = relationship("Customer", back_populates="requests")
    area = relationship("Area", back_populates="requests")
    sales_person = relationship("SalesPerson", back_populates="requests")
    stickers = relationship("Sticker", back_populates="requests")
