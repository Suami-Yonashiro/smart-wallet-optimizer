import fundamentus as fd
import pandas as pd
import math

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

resultado = df_elegivel[[
    'Cotação', 'LPA', 'VPA', 'ROE',
    'Div.Yield', 'Preco_Justo',
    'Margem_Seguranca', 'Sinal'
]].copy()

resultado = resultado.sort_values('Margem_Seguranca', ascending=False)

print("\n=== TOP 10 AÇÕES COM MAIOR MARGEM DE SEGURANÇA ===")
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
print(resultado.head(10).to_string())

print("\n=== RESUMO DOS SINAIS ===")
print(resultado['Sinal'].value_counts().to_string())

print("\n=== VALE3 ESPECIFICAMENTE ===")
if 'VALE3' in resultado.index:
    v = resultado.loc['VALE3']
    print(f"Cotação atual : R$ {v['Cotação']:.2f}")
    print(f"Preço justo   : R$ {v['Preco_Justo']:.2f}")
    print(f"Margem        : {v['Margem_Seguranca']:.2f}%")
    print(f"Sinal         : {v['Sinal']}")