from sqlalchemy import create_engine, Column, String, Integer, ForeignKey, Float
from sqlalchemy.orm import declarative_base, relationship, sessionmaker


engine = create_engine('sqlite:///market.db')
Base = declarative_base()

Session = sessionmaker(bind=engine)
session = Session()


class Category(Base):
    """Creating the table for the category of the products"""
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    category_name = Column(String(50), nullable=False)
    products = relationship("Product", back_populates='category', cascade='all, delete-orphan')
    # VAI CONTER PRODUTOS COM UMA RELACAO COM A CLASSE E UM NOME DIFERENTE PARA O BACK
    # DECLARA TAMBEM O CASCADE PARA DELETAR TODOS OS RELACIONADOS


class Product(Base):
    """Creting the table for the products, who will interact with an relashionship
    with the Category table"""
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    price = Column(Float, nullable=False)
    amount = Column(Integer)
    total = Column(Float)
    category_name = Column(String(50), ForeignKey("categories.category_name", ondelete='CASCADE'), nullable=False)
    # RECEBE A FOREIGNKEY COM A TABLENAME.NOME DA COLUNA
    entry_date = Column(String)
    exit_date = Column(String)
    category = relationship("Category", back_populates="products")
    # RECEBE UMA RELATIONSHIP COM A CLASSE E BACK_POPULATES COM A PROPRIA TABLENAME


Base.metadata.create_all(engine)