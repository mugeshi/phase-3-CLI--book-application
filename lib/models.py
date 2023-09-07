from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///bookstore.db')
Session = sessionmaker(bind=engine)
session=Session()
Base = declarative_base()


class Book(Base):
    __tablename__ = "Books"

    id = Column(Integer, primary_key=True)
    titles = Column(String, nullable=False)
    author = Column(String, nullable=False)
    genre = Column(String)
    price = Column(Integer)
    stock = Column(Integer)
    orders = relationship("Order", back_populates="book") 

class Customer(Base):
    __tablename__ = "Customer"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    contact_info = Column(String)
    orders= relationship("Order", back_populates="customer")

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('Customer.id'))
    book_id = Column(Integer, ForeignKey('Books.id'))
    quantity = Column(Integer)

    customer = relationship("Customer", back_populates="orders")
    book = relationship("Book", back_populates="orders")


