from sqlalchemy import create_engine, Column, String, Integer, ForeignKey, Float, DateTime
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from datetime import datetime

engine = create_engine('sqlite:///market.db')
Base = declarative_base()


class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    category_name = Column(String(50), nullable=False)
    products = relationship("Product", back_populates='category', cascade='all, delete-orphan')
    # VAI CONTER PRODUTOS COM UMA RELACAO COM A CLASSE E UM NOME DIFERENTE PARA O BACK
    # DECLARA TAMBEM O CASCADE PARA DELETAR TODOS OS RELACIONADOS


class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    price = Column(Float, nullable=False)
    amount = Column(Integer)
    total = Column(Float)
    category_name = Column(String(50), ForeignKey("categories.category_name", ondelete='CASCADE'), nullable=False)
    # RECEBE A FOREIGNKEY COM A TABLENAME.NOME DA COLUNA
    entry_date = Column(DateTime, default=datetime.utcnow())
    exit_date = Column(DateTime)
    category = relationship("Category", back_populates="products")
    # RECEBE UMA RELATIONSHIP COM A CLASSE E BACK_POPULATES COM A PROPRIA TABLENAME


Base.metadata.create_all(engine)