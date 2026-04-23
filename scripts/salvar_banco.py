import fundamentus as fd
import pandas as pd
import math
from sqlalchemy import create_engine
import os

print("Buscando dados da B3... aguarde...\n")
df = fd.get_resultado_raw()

print("Calculando LPA e VPA...")
df['LPA'] = df['Cotação'] / df['P/L']
df['VPA'] = df['Cotação'] / df['P/VP']

print("Aplicando filtros de elegibilidade...")
df_elegivel = df[
    (df['P/L'] > 0) &
    (df['ROE'] > 0) &
    (df['LPA'] > 0) &
    (df['Liq.2meses'] > 1000000)
].copy()

print(f"Ações elegíveis: {len(df_elegivel)}\n")

print("Calculando Preço Justo de Graham...")
def calcular_graham(row):
    try:
        valor = math.sqrt(22.5 * row['LPA'] * row['VPA'])
        return round(valor, 2)
    except:
        return None

df_elegivel['Preco_Justo'] = df_elegivel.apply(calcular_graham, axis=1)

print("Calculando Margem de Segurança...")
def calcular_margem(row):
    try:
        margem = ((row['Preco_Justo'] - row['Cotação']) / row['Preco_Justo']) * 100
        return round(margem, 2)
    except:
        return None

df_elegivel['Margem_Seguranca'] = df_elegivel.apply(calcular_margem, axis=1)

print("Classificando sinais...")
def classificar_sinal(margem):
    if margem >= 25:
        return 'COMPRAR'
    elif margem >= 0:
        return 'AGUARDAR'
    else:
        return 'EVITAR'

df_elegivel['Sinal'] = df_elegivel['Margem_Seguranca'].apply(classificar_sinal)

print("Preparando tabela final...")
from datetime import date
df_elegivel['Data_Coleta'] = date.today().strftime('%Y-%m-%d')
df_elegivel['Ticker'] = df_elegivel.index

resultado = df_elegivel[[
    'Ticker', 'Data_Coleta', 'Cotação', 'LPA', 'VPA',
    'ROE', 'Div.Yield', 'P/L', 'P/VP',
    'Preco_Justo', 'Margem_Seguranca', 'Sinal',
    'Liq.2meses', 'Patrim. Líq'
]].copy()

resultado.columns = [
    'Ticker', 'Data_Coleta', 'Cotacao', 'LPA', 'VPA',
    'ROE', 'Div_Yield', 'PL', 'PVP',
    'Preco_Justo', 'Margem_Seguranca', 'Sinal',
    'Liquidez_2meses', 'Patrimonio_Liquido'
]

resultado = resultado.reset_index(drop=True)

print("Salvando no banco de dados SQLite...")
db_path = os.path.join('data', 'smart_wallet.db')
engine = create_engine(f'sqlite:///{db_path}')

resultado.to_sql(
    name='valuation',
    con=engine,
    if_exists='replace',
    index=False
)

print(f"\nBanco criado em: {db_path}")
print(f"Tabela 'valuation' salva com {len(resultado)} ações")

print("\n=== CONFIRMANDO LEITURA DO BANCO ===")
df_verificacao = pd.read_sql("SELECT * FROM valuation LIMIT 5", engine)
print(df_verificacao[['Ticker', 'Cotacao', 'Preco_Justo', 'Margem_Seguranca', 'Sinal']].to_string())

print("\nTudo salvo com sucesso!")