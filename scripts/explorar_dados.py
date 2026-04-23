import fundamentus as fd
import pandas as pd

print("Buscando dados da B3... aguarde...\n")
df = fd.get_resultado_raw()

print("=== FORMATO DA TABELA ===")
print(f"Total de linhas (ações): {len(df)}")
print(f"Total de colunas       : {len(df.columns)}")

print("\n=== CALCULANDO LPA E VPA ===")
df['LPA'] = df['Cotação'] / df['P/L']
df['VPA'] = df['Cotação'] / df['P/VP']
print("LPA e VPA calculados com sucesso!")

print("\n=== EXEMPLO COMPLETO — VALE3 ===")
vale = df.loc['VALE3']
print(f"Cotação : R$ {vale['Cotação']:.2f}")
print(f"P/L     : {vale['P/L']:.2f}")
print(f"P/VP    : {vale['P/VP']:.2f}")
print(f"ROE     : {vale['ROE']*100:.2f}%")
print(f"LPA     : R$ {vale['LPA']:.2f}  (calculado)")
print(f"VPA     : R$ {vale['VPA']:.2f}  (calculado)")
print(f"Div.Yield: {vale['Div.Yield']*100:.2f}%")

print("\n=== VERIFICANDO QUALIDADE DOS DADOS ===")
pl_positivo = df[df['P/L'] > 0]
print(f"Ações com P/L positivo : {len(pl_positivo)}")

roe_positivo = df[df['ROE'] > 0]
print(f"Ações com ROE positivo : {len(roe_positivo)}")

lpa_positivo = df[df['LPA'] > 0]
print(f"Ações com LPA positivo : {len(lpa_positivo)}")

filtro_base = df[
    (df['P/L'] > 0) &
    (df['ROE'] > 0) &
    (df['LPA'] > 0) &
    (df['Liq.2meses'] > 1000000)
]
print(f"\nAções elegíveis para o modelo")
print(f"(P/L, ROE e LPA positivos + liquidez mínima): {len(filtro_base)} ações")