import pandas as pd
from sqlalchemy import create_engine
import os

print("Lendo banco de dados...")
engine = create_engine('sqlite:///data/smart_wallet.db')
df = pd.read_sql("SELECT * FROM valuation", engine)

print("Adicionando colunas auxiliares para o Power BI...")

df['Alerta_Margem'] = df['Margem_Seguranca'].apply(
    lambda x: 'Verificar' if x >= 60 else ''
)

df['Funil'] = 'Elegível'

df['ROE_Percent'] = (df['ROE'] * 100).round(2)
df['DY_Percent'] = (df['Div_Yield'] * 100).round(2)

print("Exportando para Excel...")
caminho = os.path.join('data', 'smart_wallet.xlsx')
df.to_excel(caminho, index=False, sheet_name='Valuation')

funil_data = {
    'Etapa': ['Total B3', 'Removidas por prejuízo', 'Removidas por ROE', 'Removidas por liquidez', 'Elegíveis'],
    'Quantidade': [997, 372, 252, 205, 168],
    'Tipo': ['total', 'exclusao', 'exclusao', 'exclusao', 'elegivel'],
    'Ordem': [1, 2, 3, 4, 5]
}
df_funil = pd.DataFrame(funil_data)

with pd.ExcelWriter(caminho, engine='openpyxl', mode='a') as writer:
    df_funil.to_excel(writer, sheet_name='Funil', index=False)

print(f"Arquivo salvo em: {caminho}")
print(f"Ações exportadas : {len(df)}")
print(f"Com alerta       : {len(df[df['Alerta_Margem'] == 'Verificar'])} ações")
print(f"Abas criadas     : Valuation + Funil")