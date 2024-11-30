from sqlalchemy import Column, Float, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from src.database import Base

class DimProduto(Base):
    __tablename__ = 'dim_products'
    id = Column(String, primary_key=True)
    produto = Column(String)
    id_familia = Column(String)
    id_grupo = Column(String)
    id_subgrupo = Column(String)
    familia_descricao = Column(String)
    grupo_descricao = Column(String)
    subgrupo_descricao = Column(String)

    #relationships
    fact_sales = relationship('FactSales', back_populates='product', cascade='all, delete-orphan')
    fact_margin = relationship('FactMargin', back_populates='product', cascade='all, delete-orphan')
    fact_storage = relationship('FactStorage', back_populates='product', cascade='all, delete-orphan')


class FactSales(Base):
    __tablename__ = 'fact_sales'
    id = Column(Integer, primary_key=True, index=True)
    id_produto = Column(String, ForeignKey('dim_products.id'))
    data = Column(DateTime)
    faturamento = Column(Float)
    quantidade = Column(Integer)

    #relationships
    produto = relationship('DimProduct', back_populates='sales')

class FactMargin(Base):
    __tablename__ = 'fact_margin'
    id = Column(Integer, primary_key=True, index=True)
    id_produto = Column(String, ForeignKey('dim_products.id'))
    data = Column(DateTime)
    valor_margem = Column(Float)

    #relationships
    produto = relationship('DimProduct', back_populates='margin')

class FactStorage(Base):
    __tablename__ = 'fact_storage'
    id = Column(Integer, primary_key=True, index=True)
    id_produto = Column(String, ForeignKey('dim_products.id'))
    data = data = Column(DateTime)
    quantidade = Column(Float)

    #relationships
    produto = relationship('DimProduct', back_populates='storage')