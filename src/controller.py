import pandas as pd
from database import SessionLocal, engine, Base
from models import DimProduto, FactMargin, FactSales, FactStorage
from schemas import DimProductSchema, FactMarginSchema, FactSalesSchema, FactStorageSchema

Base.metadata.create_all(bind=engine)

def create_df(file_path):
    df = pd.read_excel(file_path)
    return pd

