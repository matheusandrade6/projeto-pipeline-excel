import pandas as pd
import numpy as np
from pandas import DataFrame
from src.database import SessionLocal, engine, Base
from src.models import DimProduto, FactMargin, FactSales, FactStorage
from src.schemas import DimProductSchema, FactMarginSchema, FactSalesSchema, FactStorageSchema

Base.metadata.create_all(bind=engine)

# Cria um dicionário de Dataframes -> chave: sheet_name, valor: DataFrame

def load_excel(file_path: str) -> dict:
    sheets = pd.read_excel(file_path, sheet_name=None)

    return sheets

# Limpa espaços em branco no nome das colunas

def trim_column_names(df: DataFrame) -> DataFrame:
    df.columns = df.columns.str.strip()
    print('Nome das colunas limpos')
    return df

# Limpa espaços em branco nas linhas das colunas

def trim_text_columns(df: DataFrame) -> DataFrame:
    df = pd.DataFrame(df)
    for coluna in df.select_dtypes(include=['object']).columns:
        df[coluna] = df[coluna].str.strip()
    return df

def add_data_to_database(sheets_dict: dict):
    for sheet_name, df in sheets_dict.items():
        if not isinstance(df, pd.DataFrame):
            df = pd.DataFrame(df)

        print(f'Limpando as colunas de {sheet_name}')
        df = trim_column_names(df)

        print(f'Limpando o conteúdo das colunas de {sheet_name}')
        df = trim_text_columns(df)

        print(f'Adicionando os dados da planilha {sheet_name} no banco de dados')
        with SessionLocal() as db:
            if sheet_name == 'Dim_Produto':
                df = df.drop_duplicates(subset=['COD_PRODUTO'])

                produtos = []
                for index, row in df.iterrows():
                    if pd.isna(row['COD_PRODUTO']) or row['COD_PRODUTO'] == 'Total':
                        continue
                    
                    produtos.append(DimProduto(
                        id=row['COD_PRODUTO'],
                        produto=row['DESCRICAO_PRODUTO'],
                        id_familia=row['COD_FAMILIA'],
                        id_grupo=row['COD_GRUPO'],
                        id_subgrupo=row['COD_SUBGRUPO'],
                        familia_descricao=row['DESCRICAO_FAMILIA'],
                        grupo_descricao=row['DESCRICAO_GRUPO'],
                        subgrupo_descricao=row['DESCRICAO_SUBGRUPO'],
                    ))

                try:
                    db.add_all(produtos)
                    db.commit()
                except Exception as e:
                    print(f'Erro ao adicionar dados ao banco: {e}')
                    db.rollback()


            if sheet_name == 'Fat_Venda':
                vendas = []
                for index, row in df.iterrows():
                    
                    if pd.isna(row['DATA']):
                        continue
                    
                    if pd.isna(row['FATURAMENTO']) or pd.isna(row['QUANTIDADE']):
                        raise ValueError(f'Data inválida na linha {index}: {row['FATURAMENTO'], row['QUANTIDADE']}')
                        continue

                    vendas.append(FactSales(
                        id_produto=row['COD_PRODUTO'],
                        data=row['DATA'],
                        faturamento=row['FATURAMENTO'],
                        quantidade=row['QUANTIDADE'],
                    ))
                try:
                    db.add_all(vendas)
                    db.commit()
                except Exception as e:
                    print(f'Erro ao adicionar dados ao banco: {e}')
                    db.rollback()

            if sheet_name == 'Fat_Margem':
                margem = []

                for index, row in df.iterrows():

                    if pd.isna(row['DATA']):
                        continue

                    if pd.isna(row['COD_PRODUTO']) or row['COD_PRODUTO'] == 'Total':
                        continue

                    margem.append(FactMargin(
                        id_produto=row['COD_PRODUTO'],
                        data=row['DATA'],
                        valor_margem=row['MG VALOR'],
                    ))
                
                try:
                    db.add_all(margem)
                    db.commit()
                except Exception as e:
                    print(f'Erro ao adicionar dados ao banco: {e}')
                    db.rollback()

            if sheet_name == 'Fat_Estoque':
                estoque = []

                for index, row in df.iterrows():
                    if pd.isna(row['COD_PRODUTO']) or row['COD_PRODUTO'] == 'Total':
                        continue
                    estoque.append(FactStorage(
                        id_produto=row['COD_PRODUTO'],
                        quantidade=row['EST_QTDE'],
                    ))

                try:
                    db.add_all(estoque)
                    db.commit()
                except Exception as e:
                    print(f'Erro ao adicionar dados ao banco: {e}')
                    db.rollback()
